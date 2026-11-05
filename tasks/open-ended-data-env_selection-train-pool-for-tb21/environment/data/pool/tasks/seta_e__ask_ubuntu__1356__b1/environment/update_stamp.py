import dnf
import time


class UpdateStamp(dnf.Plugin):
    name = 'update_stamp'

    def __init__(self, base, cli):
        super(UpdateStamp, self).__init__(base, cli)

    def resolved(self):
        with open('/var/cache/dnf/update-stamp', 'w') as f:
            f.write(str(int(time.time())))
