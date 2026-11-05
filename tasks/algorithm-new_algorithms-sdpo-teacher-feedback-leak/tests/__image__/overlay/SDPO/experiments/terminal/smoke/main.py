"""Entry point of the smoke run (see experiments/terminal/run_sdpo_terminal_smoke.sh): verl.trainer.main_ppo with the
smoke config and the smoke TaskRunner."""

from pathlib import Path

import hydra
import ray

import verl
from verl.trainer.main_ppo import run_ppo
from verl.utils.device import auto_set_device

CONFIG_DIR = str(Path(verl.__file__).resolve().parent / "trainer" / "config")


@hydra.main(config_path=CONFIG_DIR, config_name="sdpo_terminal_smoke", version_base=None)
def main(config):
    auto_set_device(config)
    from experiments.terminal.smoke.runner import SmokeTaskRunner

    run_ppo(config, task_runner_class=ray.remote(num_cpus=1)(SmokeTaskRunner))
    ray.shutdown()  # stop the rollout servers and workers now rather than at interpreter exit


if __name__ == "__main__":
    main()
