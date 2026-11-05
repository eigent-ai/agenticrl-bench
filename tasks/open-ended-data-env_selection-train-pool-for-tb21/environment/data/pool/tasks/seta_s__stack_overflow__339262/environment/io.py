"""CSV I/O for matrix files."""
import csv
import os


def read_matrix_csv(filepath):
    """Read a CSV file and return a list of lists representing the matrix.

    Args:
        filepath: path to a CSV file with numeric values.

    Returns:
        list of lists of values.
    """
    matrix = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                matrix.append([v.strip() for v in row])
    return matrix


def write_matrix_csv(matrix, filepath):
    """Write a matrix (list of lists) to a CSV file.

    Args:
        matrix: list of lists of numeric values.
        filepath: output file path.
    """
    d = os.path.dirname(filepath)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in matrix:
            writer.writerow(row)
