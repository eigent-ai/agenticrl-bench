import os
import runpy
import argv
from gpu_argv import to_baseline
_recipe = argv.build_argv
argv.build_argv = lambda case, **kw: to_baseline(_recipe(case, **kw))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rollout_stage.py"), run_name="__main__")
