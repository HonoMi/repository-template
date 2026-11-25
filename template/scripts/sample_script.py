import logging
from copy import deepcopy

import fire

logger = logging.getLogger(__name__)


def main(output_dir: str,
         param_0=0,
         param_1=0,
         n_cpus: int = None):
    # (...)
    logger.info('-------------- sample_script.py finished --------------')


if __name__ == "__main__":
    try:
        from logger_setup import setup as setup_logger
        setup_logger()
    except ImportError:
        logging.basicConfig(level=logging.INFO)
    setup_logger()
    fire.Fire(main)
