import os
import runpy
import sys
argv = sys.argv[1:]
paths = []
while argv[:1] == ["--path"]:
    paths.append(argv[1])
    argv = argv[2:]
sys.path[:] = paths + [p for p in sys.path
                       if not (os.path.realpath(p or ".") + "/").startswith(("/app/", "/tmp/", "/home/"))]
sys.meta_path[:] = [f for f in sys.meta_path
                    if not ("__editable__" in str(getattr(f, "__module__", "")) and "miles" in str(f.__module__))]
if argv[:1] == ["--module"]:
    sys.argv = argv[1:]
    runpy.run_module(argv[1], run_name="__main__", alter_sys=True)
else:
    sys.argv = argv
    runpy.run_path(argv[0], run_name="__main__")
