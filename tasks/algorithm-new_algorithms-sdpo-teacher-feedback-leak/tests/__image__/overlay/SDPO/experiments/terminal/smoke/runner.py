"""TaskRunner for the smoke run: the standard one, with the teacher-context dump installed in the trainer process."""

import traceback

from verl.trainer.main_ppo import TaskRunner


class SmokeTaskRunner(TaskRunner):
    def run(self, config):
        from experiments.terminal.smoke import dump

        dump.start(config)
        try:
            super().run(config)
        except BaseException:
            dump.finish(ok=False, error=traceback.format_exc())
            raise
        dump.finish(ok=True)
