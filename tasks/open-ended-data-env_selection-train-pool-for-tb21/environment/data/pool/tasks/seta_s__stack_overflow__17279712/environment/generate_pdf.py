#!/usr/bin/env python3
"""Generate a simple PDF file from scratch."""
import sys

def generate_pdf(output_path):
    """Generate a minimal valid PDF with a single page containing text."""

    objects = []

    # Object 1: Catalog
    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    objects.append(obj1)

    # Object 2: Pages
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    objects.append(obj2)

    # Object 3: Page
    obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    objects.append(obj3)

    # Object 4: Content stream
    stream_content = b"BT /F1 12 Tf 100 700 Td (Hello PDF World) Tj ET"
    obj4 = b"4 0 obj\n<< /Length " + str(len(stream_content)).encode() + b" >>\nstream\n" + stream_content + b"\nendstream\nendobj\n"
    objects.append(obj4)

    # Object 5: Font
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    objects.append(obj5)

    # Build PDF
    header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    body = b""
    offsets = []

    for obj in objects:
        offsets.append(len(header) + len(body))
        body += obj

    # Build xref table
    xref = b"xref\n"
    xref += f"0 {len(objects) + 1}\n".encode()
    xref += b"0000000000 00000 f\r\n"
    for offset in offsets:
        xref += f"{offset:07d} 00000 n\r\n".encode()

    # Compute startxref
    startxref_value = len(body)

    # Trailer
    trailer = b"trailer\n"
    trailer += f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode()
    trailer += b"startxref\n"
    trailer += f"{startxref_value}\n".encode()
    trailer += b"%%EOF\n"

    with open(output_path, 'wb') as f:
        f.write(header)
        f.write(body)
        f.write(xref)
        f.write(trailer)

    print(f"Generated PDF: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_pdf.py <output_path>")
        sys.exit(1)
    generate_pdf(sys.argv[1])
