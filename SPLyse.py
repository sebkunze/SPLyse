#!/usr/bin/env python
import os

from argparse    import ArgumentParser
from subprocess  import call

from core        import parser, runner, solver
from core.utils  import constants, logger, misc


def main():
    # creating console interface
    command_line = ArgumentParser(description="analyser for software product lines.")

    # adding positional arguments.
    command_line.add_argument("directory", help="input source file directory.")

    # adding optional argument for variants.
    command_line.add_argument("-v", "--variants", help="software product line variants", nargs="+")

    # adding optional argument for method.
    command_line.add_argument("-m", "--method", help="variant method.")

    # adding optional argument for tasks.
    group = command_line.add_mutually_exclusive_group()
    group.add_argument("-a", "--analyse-states",action="store_true", help="analyse individual program execution paths.")
    group.add_argument("-g", "--compare-states",  action="store_true", help="analyse individual program execution paths and guide test analysis.", default=1)

    # populating parser.
    options = command_line.parse_args()

    print 'PREPARING WORKSPACE.'

    # create subdirectory for workspace or clean it up if existing.
    misc.set_up_workspace(constants.workspace)

    # find variants information.
    print 'SEARCHING SOURCES.'

    # look up variants' source files in specified directory.
    sources = misc.look_up_sources(options.directory, options.variants)

    print 'PARSING SOURCE FILES.'

    # translate JAVA source files to BOOGIE source files
    parser.translate_source_files(sources)

    print 'EXECUTING CODE SYMBOLICALLY.'

    # generate terminated states of BOOGIE files using SYMBOOGLIX
    runner.generate_terminated_states(options.method)

    print 'ANALYSING TERMINATED STATES.'

    if options.analyse_states:
        solver.analyse()
    elif options.compare_states:
        solver.guide()

    print 'DONE'


if __name__ == '__main__':
    main()