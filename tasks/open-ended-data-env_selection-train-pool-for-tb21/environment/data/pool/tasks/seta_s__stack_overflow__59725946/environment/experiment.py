import os, sys, time
restart = int(os.environ.get("SLURM_RESTART_COUNT", "0"))
task_id = os.environ.get("SLURM_ARRAY_TASK_ID", "0")
time.sleep(0.1)
if restart == 0:
    print(f"Experiment task {task_id}: transient GPU memory error, exiting 42")
    sys.exit(42)
print(f"Experiment task {task_id}: success on restart {restart}")
print("COMPLETE")
