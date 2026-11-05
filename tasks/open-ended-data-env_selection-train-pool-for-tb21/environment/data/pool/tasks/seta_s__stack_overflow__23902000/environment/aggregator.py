"""Aggregate sensor data statistics."""

import json


def aggregate(data, channel_count):
    """Compute per-channel statistics from parsed sensor data.

    Args:
        data: List of rows, each row is a list of float values
        channel_count: Number of sensor channels

    Returns:
        Dictionary with per-channel min, max, mean, count
    """
    stats = {}
    for ch in range(channel_count):
        ch_values = [row[ch] for row in data if ch < len(row)]
        if ch_values:
            stats[f'channel_{ch}'] = {
                'min': min(ch_values),
                'max': max(ch_values),
                'mean': sum(ch_values) / len(ch_values),
                'count': len(ch_values)
            }
    return stats


def write_summary(filepath, all_stats):
    """Write aggregated statistics to a JSON summary file."""
    with open(filepath, 'w') as f:
        json.dump(all_stats, f, indent=2)
