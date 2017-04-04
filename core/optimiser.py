import os, sys
import logging

from subprocess             import call

from core.utils             import constants, misc
from core.utils.progressbar import ProgressBar


# get logging instance.
log = logging.getLogger('SPLyse')

# get progress bar instance.
bar = ProgressBar()

def adjust_test_cases(testinfos, testcases): # TODO: Use one dict instead!
    size = len(testinfos.items())

    # setup progressbar's size.
    bar.setup(size)

    # print skeleton.
    bar.skeleton()

    for to_be_tested, infos in testinfos.items():

        for already_tested, cases in testcases.items():

            if to_be_tested == already_tested:
                continue

            for path_to_test_info in infos:

                for path_to_test_case in cases:
                    # TODO: Allow for more generic test file names.
                    _, last = os.path.split(path_to_test_case);
                    if not last == "SPLyse.java":
                        continue

                    target \
                        = os.path.join(constants.workspace
                                   , to_be_tested
                                   , already_tested + '.yml')

                    cmd = \
                        [ constants.OPTIMISER
                        , '--testcase'
                        , path_to_test_case
                        , '--testinfo'
                        , path_to_test_info
                        , '--target'
                        , target
                        ]

                    call(misc.to_command(cmd), shell=True)

        # print progress.
        bar.progress()

    # print done.
    bar.done()
