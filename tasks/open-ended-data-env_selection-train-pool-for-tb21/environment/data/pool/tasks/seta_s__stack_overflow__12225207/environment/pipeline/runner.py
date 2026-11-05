import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solvers.gauss_seidel import gauss_seidel
from solvers.sor import sor
from solvers.convergence import check_convergence_conditions
from solvers.utils import compute_residual
from pipeline.analyzer import analyze_convergence


def load_systems(data_path):
    """Load linear systems from JSON data file."""
    with open(data_path, 'r') as f:
        data = json.load(f)
    return data["systems"]


def run_solver(solver_func, solver_name, A, b, x0, **kwargs):
    """Run a single solver and collect results."""
    x, iterations, converged, residuals = solver_func(A, b, x0.copy(), **kwargs)
    residual_norm = compute_residual(A, x, b)
    analysis = analyze_convergence(residuals)
    return {
        "solver": solver_name,
        "solution": x.tolist(),
        "iterations": int(iterations),
        "converged": bool(converged),
        "diverged": False,
        "residual_norm": float(residual_norm),
        "convergence_analysis": analysis
    }


def run_pipeline(data_path, output_path):
    """Run the full solver pipeline on all systems."""
    systems = load_systems(data_path)
    all_results = []

    for system in systems:
        name = system["name"]
        A = np.array(system["A"], dtype=float)
        b = np.array(system["b"], dtype=float)
        n = len(b)
        x0 = np.zeros(n)

        conditions = check_convergence_conditions(A)

        gs_result = run_solver(gauss_seidel, "gauss_seidel", A, b, x0)
        gs_result["system"] = name
        gs_result["convergence_conditions"] = conditions
        all_results.append(gs_result)

        sor_result = run_solver(sor, "sor", A, b, x0, w=1.5)
        sor_result["system"] = name
        sor_result["convergence_conditions"] = conditions
        all_results.append(sor_result)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump({"results": all_results}, f, indent=2, allow_nan=False)

    return all_results
