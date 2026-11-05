import pathlib
import sys

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for p in sorted(src.glob("*.md")):
    body = []
    for ln in p.read_text().splitlines():
        if ln.startswith("# "):
            body.append(f"<h1>{ln[2:]}</h1>")
        elif ln.strip():
            body.append(f"<p>{ln}</p>")
    (out / (p.stem + ".html")).write_text("<html><body>\n" + "\n".join(body) + "\n</body></html>\n")
    print("built", p.stem + ".html")
