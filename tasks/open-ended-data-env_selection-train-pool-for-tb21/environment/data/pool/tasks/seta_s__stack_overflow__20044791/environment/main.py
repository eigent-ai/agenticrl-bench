import os
from game_engine.simulation import Simulation


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scenario_path = os.path.join(base_dir, "scenarios", "multi_enemy.json")
    sim = Simulation(scenario_path)

    sim.run(30)

    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sim_log.json")
    sim.save_log(output_path)
    print(f"Simulation complete. Log written to {output_path}")


if __name__ == "__main__":
    main()
