#!/usr/bin/env python

import os

from argparse    import ArgumentParser
from core        import optimiser, parser, runner, solver
from core.utils  import constants, misc


def main():
    # creating console interface
    command_line = ArgumentParser(description="analyser for software product lines.")

    # adding positional arguments.
    command_line.add_argument("directory", help="input source file directory.")

    # adding optional argument for specifying variants.
    command_line.add_argument("-v", "--variants", help="software product line variants", nargs="+")

    # adding optional argument for providing method.
    command_line.add_argument("-m", "--method", help="variant method")

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

    print 'SEARCHING SOURCES.'

    # look up variants' sources.
    sources = misc.look_up_sources(options.directory, options.variants, options.test_sources)

    # check empty sources.
    if not sources.items():
        print '> ERROR: CANNOT FIND SOURCES.'
        return

    print 'PREPARING WORKSPACE.'

    # create subdirectory for workspace.
    misc.set_up_workspace(constants.workspace)

    if not options.skip_translation:
        # remove all files and folders in the worlspace directory.
        misc.clear_workspace(constants.workspace)
    else:
        # remove all files and folders in the solver subdirectory.
        misc.clean_workspace(constants.workspace)

    if not options.skip_translation:
        print 'PARSING SOURCE FILES.\t\t',

        # translate JAVA source files to BOOGIE source files
        parser.translate_source_files(sources)

        print 'EXECUTING CODE SYMBOLICALLY.\t',

        # generate terminated states of BOOGIE files using SYMBOOGLIX
        runner.generate_terminated_states(options.method)
    else:
        # TODO: Check if all required variants are translated.
        s = 'undefined'

    print 'ANALYSING TERMINATED STATES.\t',

    if options.analyse_programs:
        solver.analyse()
    elif options.compare_programs:
        solver.compare()
    elif options.explore_programs:
        infos = \
            solver.compare()

        cases =\
            misc.look_up_test_files(options.directory, options.variants) # TODO: Rename to test sources!

        print "ADJUSTING TEST CASES.\t\t",

        optimiser.adjust_test_cases(infos, cases)


if __name__ == '__main__':
    main()
