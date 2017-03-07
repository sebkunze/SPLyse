#!/usr/bin/env python
import os

from argparse    import ArgumentParser
from core        import parser, runner, solver
from core.utils  import constants, misc


def main():
    # creating console interface
    command_line = ArgumentParser(description="analyser for software product lines.")

    # adding positional arguments.
    command_line.add_argument("directory", help="input source file directory")

    # adding optional argument for specifying variants.
    command_line.add_argument("-v", "--variants", help="software product line variants", nargs="+")

    # adding optional argument for providing method.
    command_line.add_argument("-m", "--method", help="variant method")

    # adding optional argument for parsing test cases.
    command_line.add_argument("-t", "--test-sources", action="store_true", help="include test source folder")

    # adding optional argument for tasks.
    group = command_line.add_mutually_exclusive_group()
    group.add_argument("-a", "--analyse-programs", action="store_true", help="analyse individual program execution paths.")
    group.add_argument("-c", "--compare-programs", action="store_true", help="analyse individual program execution paths and compare them pairwise.")
    group.add_argument("-e", "--explore-programs", action="store_true", help="analyse individual program execution paths, compare them pairwise, and explore test trajectories.")

    # populating parser.
    options = command_line.parse_args()

    print 'PREPARING WORKSPACE.'

    # create subdirectory for workspace or clean it up if existing.
    misc.set_up_workspace(constants.workspace)

    # find variants information.
    print 'SEARCHING SOURCES.'

    # look up variants' source files in specified directory.
    sources = misc.look_up_source_files(options.directory, options.variants)

    # look up variants' test files in specified directory.
    if options.test_sources:
        tests = misc.look_up_test_files(options.directory, options.variants)
        for k,v in tests.items():
            sources[k] += v

    print 'PARSING SOURCE FILES.'

    # translate JAVA source files to BOOGIE source files
    parser.translate_source_files(sources)

    print 'EXECUTING CODE SYMBOLICALLY.'

    # generate terminated states of BOOGIE files using SYMBOOGLIX
    runner.generate_terminated_states(options.method)

    print 'ANALYSING TERMINATED STATES.'

    if options.analyse_programs:
        solver.analyse()
    elif options.compare_programs:
        solver.compare()
    elif options.explore_programs:
        solver.explore()

    print 'DONE.'


if __name__ == '__main__':
    main()