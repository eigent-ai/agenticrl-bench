# Terrain Toolkit

A Python-based 3D terrain mesh processing and physics simulation toolkit for game development and terrain analysis.

## Project Structure

```
terrain_toolkit/
├── src/terrain_toolkit/
│   ├── vectors.py           # Basic 3D vector operations (dot, cross, normalize, rejection)
│   ├── mesh.py              # OBJ mesh loading, face/vertex normal computation
│   ├── projection.py        # Point-to-line projection, nearest point on segment
│   ├── navmesh.py           # Navigation mesh generation, edge bisector planes
│   └── terrain_analysis.py  # Slope analysis, traversability, path feasibility
├── scripts/
│   └── analyze_terrain.py   # CLI tool for terrain analysis reports
├── meshes/
│   └── volcano_island.obj   # Test terrain mesh with varied topology
├── tests/
│   └── test_toolkit.py      # Comprehensive test suite
└── output/
    └── terrain_report.json  # Generated analysis report
```

## Module Responsibilities

### vectors.py
Core 3D vector math operations used throughout the toolkit:
- `dot(a, b)`: Dot product of two vectors
- `cross_product(a, b)`: Cross product following the right-hand rule
- `normalize(v)`: Returns unit-length vector
- `magnitude(v)`: Returns vector length
- `vector_rejection(v, n)`: Projects vector v onto the plane with normal n. For arbitrary (non-unit) normals, the correct formula is: `v - (dot(v,n)/dot(n,n)) * n`. This is essential for computing movement vectors that slide along terrain surfaces rather than clipping through them.

### mesh.py
Mesh I/O and normal computation:
- `load_obj(filepath)`: Parses Wavefront OBJ files (vertices and triangular faces)
- `compute_face_normal(vertices, face)`: Computes the unit normal of a triangle using edge cross product
- `compute_face_area(vertices, face)`: Computes triangle area via cross product magnitude
- `compute_vertex_normals(vertices, faces)`: Computes smooth vertex normals by **area-weighted** averaging of adjacent face normals. Each face's contribution to a vertex normal must be weighted by the face's area so that large triangles have proportionally more influence than small ones.

### projection.py
Geometric projection operations:
- `nearest_point_on_segment(point, seg_start, seg_end)`: Finds the closest point on a finite line segment. The parametric value t must be clamped to [0, 1] to ensure the result lies on the segment, not the infinite line.
- `point_to_plane_distance(point, plane_point, plane_normal)`: Signed distance from point to plane.

### navmesh.py
Navigation mesh generation for pathfinding:
- `edge_bisector_plane(p0, p1, p2)`: Computes the bisector plane of edge (p0,p1) facing toward vertex p2. Uses the double cross product: `cross(edge, cross(edge, opposite_edge))` where `edge = p1-p0` and `opposite_edge = p2-p0`. The result must be normalized.
- `compute_corridor(triangles, shared_edge_indices)`: Builds navigation corridors from triangle sequences.

### terrain_analysis.py
High-level terrain analysis:
- `compute_slope_angle(normal)`: Computes slope angle in degrees from a surface normal. The slope angle is the angle between the surface and horizontal, which equals `arccos(dot(normal, up))` for **unit-length** normals.
- `classify_traversability(slope_angle)`: Classifies terrain into categories:
  - `easy`: 0-15°
  - `moderate`: 15-30°
  - `difficult`: 30-45°
  - `untraversable`: > 45°
- `check_path_feasibility(...)`: Evaluates whether a path between two points is walkable.
- `analyze_terrain(obj_path, output_path)`: Full pipeline producing JSON report.

## Usage

```bash
# Run all tests
python -m pytest tests/ -v

# Analyze a terrain mesh
python scripts/analyze_terrain.py meshes/volcano_island.obj

# Output is written to output/terrain_report.json
```

## Dependencies

- Python 3.12+
- NumPy
