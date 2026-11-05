"""Stage 3: Summarization.

Creates summary dictionaries and nested structures from computed results.
Includes a helper function whose locals should also be captured.
"""

from varinspect.capture import capture_variables, capture_locals_from_frame


def _format_output(title, items):
    """Helper function that formats output for the summary.

    Its local variables should be captured via nested frame inspection.
    """
    header = f"=== {title} ==="
    formatted_lines = [f"  - {k}: {v}" for k, v in items.items()]
    body = "\n".join(formatted_lines)
    total_items = len(items)
    nested_locals = capture_locals_from_frame(depth=1)
    return {
        "formatted": f"{header}\n{body}",
        "item_count": total_items,
        "nested_variables": nested_locals,
    }


def summarize():
    """Run the summarization stage.

    Returns:
        dict: Captured variables from this stage.
    """
    summary_table = {
        "preprocess": {"records_processed": 4, "mean_value": 39.22},
        "compute": {"weighted_sum": 38.59, "n_values": 4},
    }

    final_metrics = {
        "total_stages": 3,
        "pipeline_status": "complete",
        "quality_score": 0.92,
    }

    output_sections = ["overview", "details", "appendix"]

    detail_items = {
        "alpha": 23.5,
        "beta": 47.1,
        "delta": 55.3,
        "epsilon": 31.0,
    }

    formatted_result = _format_output("Analysis Summary", detail_items)

    conclusion = "Pipeline completed successfully with 4 records across 3 stages."

    return capture_variables(tag="summarize")
