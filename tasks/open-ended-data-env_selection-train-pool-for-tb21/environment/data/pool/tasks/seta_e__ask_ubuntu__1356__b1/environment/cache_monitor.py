import dnf
import configparser
import os


class CacheMonitor(dnf.Plugin):
    name = 'cache_monitor'

    def __init__(self, base, cli):
        super(CacheMonitor, self).__init__(base, cli)
        config_path = '/etc/dnf/plugins/cache_monitor.conf'
        if not os.path.isfile(config_path):
            raise dnf.exceptions.Error(
                'Cache monitor plugin: configuration file {} not found!'.format(config_path)
            )
        config = configparser.ConfigParser()
        config.read(config_path)
