#!/usr/bin/env python
import logging
from pathlib import Path
from itertools import product
import json
import textwrap

from script_engine import SubprocessEngine, QsubEngine, run_by_engine
from logger_setup import setup as setup_logger
from lab import build_dir, cli_arg


from settings import get_model_path



logger = logging.getLogger(__name__)


def main():
    # AGENT: このスクリプトでは、見やすさのため、改行を十分に取る。
    setup_logger(level=logging.INFO, clear_other_handlers=True)




    output_top_dir = Path('./outputs/00.exp.py/2026-04-27.test')



    model_name_sweep = [
        'model_0',
        'model_1',
    ]




    param_0_sweep = [
        0,
        1,
        2,
    ]




    param_1_sweep = [
        0,
        1,
        2,
    ]




    # engine = SubprocessEngine('kokubunji-2024', 'xhn_s.small', n_resource=1)
    # engine = QsubEngine('kokubunji-2024', 'xhn_dev.middle', n_resource=1)


    engine = QsubEngine('kokubunji-2024', 'xhn_s.small', n_resource=1)
    # engine = QsubEngine('kokubunji-2024', 'xhn_s.middle', n_resource=1)
    # engine = QsubEngine('kokubunji-2024', 'xhn_s.middle2', n_resource=1)























    # ------------------------------------- fixed settings -----------------------------------------


    dry_run = False
    debug = None

    skip_if_exists = False

    hours = 4 if engine.resource.find('dev') >= 0 else 24



    _debug = debug or isinstance(engine, SubprocessEngine)
    if _debug:
        do_log_on_host_run = False
        wait_until_finish = True
        tee_log = True
    else:
        do_log_on_host_run = True
        wait_until_finish = False
        tee_log = False
    num_cpus = engine.num_cpus
    num_gpus = engine.num_gpus


    param_sets = product(
        model_name_sweep,
        param_0_sweep,
        param_1_sweep,
    )

    for (model_name,
         param_0,
         param_1) in param_sets:


        setting = {
            'model_name': model_name,
            'model_path': get_model_path(model_name),
            'param_0': param_0,
            'param_1': param_1,
            'num_cpus': num_cpus,
            'num_gpus': num_gpus,
        }


        output_dir = build_dir(
            setting,
            top_dir=output_top_dir,
            short=True,
            dirname_ignore_params = [
                # long params here
                'model_path',
            ],
        )


        command = ' '.join([
            'source ./set-envs.sh;',

            'python ./scripts/sample_script.py',

            # AGENT: 可能な限り、settingから取ること。
            cli_arg('output_dir', setting['output_dir']),
            cli_arg('model_path', setting['model_path']),
            cli_arg('param_0', setting['param_0']),
            cli_arg('param_1', setting['param_1']),
            cli_arg('num_cpus', setting['num_cpus']),
            cli_arg('num_gpus', setting['num_gpus']),
        ])


        run_by_engine(
            engine,
            command,
            output_dir,
            other_options={'n_opt': 'R26P0160'},
            hours=hours,
            wait_until_finish=wait_until_finish,
            do_log_on_host_run=do_log_on_host_run,
            tee_log=tee_log,
            dry_run=dry_run,
            skip_if_exists=skip_if_exists,
        )

    logger.info('------------- ./00.exp.py finished -------------')


if __name__ == '__main__':
    main()
