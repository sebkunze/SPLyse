#!/usr/bin/env python
import time

from argparse    import ArgumentParser
from core        import optimiser, parser, runner, solver
from core.utils  import constants, logger, misc, report

# setup logging mechanism.
logger.setup(constants.log_file_path)

def main():
    # creating console interface
    command_line = ArgumentParser(description="analyser for software product lines.")

    # adding positional arguments.
    command_line.add_argument("directory", help="input source file directory.")

    # adding optional argument for specifying variants.
    command_line.add_argument("-v", "--variants", help="software product line variants", nargs="+")

    # adding optional argument for providing method.
    command_line.add_argument("-m", "--method", help="variant method")

    # adding optional argument for providing method.
    command_line.add_argument("-s", "--source", help="base variant")

    # adding optional argument for parsing test cases.
    command_line.add_argument("-t", "--test-sources", action="store_true", help="include test source folder.")

    # adding optional argument for skipping code translation and code execution.
    command_line.add_argument("--skip-translation", action="store_true", help="skip translation of source files.")

    # TODO: adding optional argument for skipping comparison.

    # TODO: add option for listing all software product line variants.

    # adding optional argument for tasks.
    group = command_line.add_mutually_exclusive_group()
    group.add_argument("-a", "--analyse-programs", action="store_true", help="analyse individual program execution paths.")
    group.add_argument("-c", "--compare-programs", action="store_true", help="analyse individual program execution paths and compare them pairwise.")
    group.add_argument("-e", "--explore-programs", action="store_true", help="analyse individual program execution paths, compare them pairwise, and explore test trajectories.")

    # populating parser.
    options = command_line.parse_args()

    if not options.variants:
        print '> ERROR: NO VARIANT(S) SPECIFIED.'
        return

    if not options.method:
        print '> ERROR: NO METHOD SPECIFIED.'
        return


    # ----------------------
    # STEP 1: SEARCH SOURCES
    # ----------------------

    print 'SEARCHING SOURCES.'

    # look up variants' sources.
    sources = misc.look_up_sources(options.directory, options.variants, options.test_sources)

    # check empty sources.
    if not sources.items():
        print '> ERROR: CANNOT FIND SOURCES.'
        return


    # -------------------------
    # STEP 2: PREPARE WORKSPACE
    # -------------------------

    print 'PREPARING WORKSPACE.'

    # create subdirectory for workspace.
    misc.set_up_workspace(constants.workspace)

    if not options.skip_translation:
        # remove all files and folders in the worlspace directory.
        misc.clear_workspace(constants.workspace)
    else:
        # remove all files and folders in the solver subdirectory.
        misc.clean_workspace(constants.workspace)


    # ----------------------------------
    # STEP 3: GENERATE TERMINATED STATES
    # ----------------------------------

    if not options.skip_translation:

        # ----------------------------
        # STEP 3.A: PARSE SOURCE FILES
        # ----------------------------

        print 'PARSING SOURCE FILES.\t\t',

        # start measuring overall translation time.
        start_time = time.time()

        # translate JAVA source files to BOOGIE source files
        parser.translate_source_files(sources)

        # store overall translation time.
        report.store_time('overall_translation_time', time.time() - start_time)


        # -----------------------------------
        # STEP 3.B: EXECUTE CODE SYMBOLICALLY
        # -----------------------------------

        print 'EXECUTING CODE SYMBOLICALLY.\t',

        # start measuring overall execution time.
        start_time = time.time()

        # generate terminated states of BOOGIE files using SYMBOOGLIX
        execution_times = \
            runner.generate_terminated_states(options.method)

        # store overall execution time.
        report.store_time('overall_execution_time', time.time() - start_time)

        # store each variant's execution time.
        report.store('execution_times', execution_times)

    else:
        # TODO: Check if all required variants are translated.
        s = 'undefined'


    # ---------------------------------
    # STEP 4: ANALYSE TERMINATED STATES
    # ---------------------------------

    print 'ANALYSING TERMINATED STATES.\t',

    if options.analyse_programs:

        # start measuring overall analysis time.
        start_time = time.time()

        solver.analyse()

        # store overall analysis time.
        report.store_time('overall_analysis_time', time.time() - start_time)

    elif options.compare_programs or options.explore_programs:

        # start measuring overall comparison time.
        start_time = time.time()

        infos = solver.compare(options.source)

        # store overall comparison time.
        report.store_time('overall_comparison_time', time.time() - start_time)

    else:

        print "ERROR!"

    # ----------------------------------
    # STEP 4: ADJUST EXISTING TEST CASES
    # ----------------------------------

    if options.explore_programs:

        cases =\
            misc.look_up_test_files(options.directory, options.variants) # TODO: Rename to test sources!

        print "ADJUSTING TEST CASES.\t\t",

        # start measuring exploration comparison time.
        start_time = time.time()

        optimiser.adjust_test_cases(infos, cases)

        # store overall exploration time.
        report.store_time('overall_adjustment_time', time.time() - start_time)

    # save report.
    report.dump()


if __name__ == '__main__':
    main()
