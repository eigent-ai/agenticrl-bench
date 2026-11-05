import configparser
import os

_cfg = configparser.ConfigParser()
_cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blas_config.ini'))

OMP_NUM_THREADS = int(_cfg['threading']['omp_num_threads'])
os.environ['OMP_NUM_THREADS'] = str(OMP_NUM_THREADS)
