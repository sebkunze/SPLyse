import os
import time
import logging

from collections            import defaultdict
from subprocess             import Popen, call, check_call, check_output, CalledProcessError, STDOUT, PIPE

from core.utils             import constants, misc, report
from core.utils.progressbar import ProgressBar

# get logging instance.
log = logging.getLogger('SPLyse')

# get progress bar instance.
bar = ProgressBar()

def analyse():
    size = len(os.listdir(constants.workspace))

    # setup progressbar's size.
    bar.setup(size)

    # print skeleton.
    bar.skeleton()

    # initialise report for analysis of variants.
    analysis_report = {}

    # browse all terminated states of the software product line variant.
    for to_be_analysed_program_folder in os.listdir(constants.workspace):
        subdirectory \
            = os.path.join( constants.workspace
                          , to_be_analysed_program_folder
                          , constants.constraint_solver_output_directory)

        # create subdirectory.
        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory, 0755)

        # specify input files.
        input_files \
            = os.path.join( constants.workspace
                          , to_be_analysed_program_folder
                          , constants.symbooglix_output_directory
                          , 'terminated_states'
                          , constants.constraint_solver_source_file)

        # specify output file.
        output_directory \
            = os.path.join( constants.workspace
                          , to_be_analysed_program_folder
                          , constants.constraint_solver_output_directory)

        # specify report file.
        report_file \
            = os.path.join( constants.workspace
                          , to_be_analysed_program_folder
                          , 'report.json')

        # build command for CONSTRAINT_SOLVER.
        cmd = [ 'ConstraintSolver.py'
              , input_files
              , '--analyse-states'
              , '--report ' + report_file
              , '--target ' + output_directory]

        # start measuring analysis time
        start_time = time.time()

        # call CONSTRAINT_SOLVER.
        call(misc.to_command(cmd), shell=True)

        # store analysis time
        analysis_report[to_be_analysed_program_folder] = "{:.3f} seconds".format(time.time() - start_time)

        # print progress.
        bar.progress()

    # store analysis report.
    report.store("analysis_time", analysis_report)

    # print done.
    bar.done()


def compare(base):
    # declare dictionary storing results' file path.
    destinations = defaultdict(list)

    # lookup number of variant directories.
    number_of_variant_directories \
        = len(os.listdir(constants.workspace))

    if number_of_variant_directories == 1:
        print "> ERROR: TOO FEW VARIANTS FOR COMPARISON."
        return destinations

    # setup progressbar's size.
    bar.setup(number_of_variant_directories)

    # print skeleton.
    bar.skeleton()

    # initialise report for comparison of variants.
    comparison_report = {}

    try:
        # browse all terminated states of the software product line variant.
        for to_be_tested_program_folder in [folder for folder in os.listdir(constants.workspace) if not folder == base and not folder == ".DS_STORE"]:

            # set up path to subdirectory.
            subdirectory \
                = os.path.join( constants.workspace
                              , to_be_tested_program_folder
                              , constants.constraint_solver_output_directory)

            # create subdirectory.
            if not os.path.exists(subdirectory):
                os.makedirs(subdirectory, 0755)

            # specify terminated states of the to be tested variant.
            terminated_states_file_of_to_be_tested_variant \
                = os.path.join( constants.workspace
                              , to_be_tested_program_folder
                              , constants.symbooglix_output_directory
                              , constants.symbooglix_terminated_states_directory
                              , constants.constraint_solver_source_file)

            # collect folders of already tested programs.
            already_tested_program_folders \
                = [base] if base is not None else [folder for folder in os.listdir(constants.workspace) if not folder == to_be_tested_program_folder and not folder == ".DS_STORE"]

            for already_tested_program_folder in already_tested_program_folders:

                # specify terminated states of already test variant.
                terminated_states_of_already_tested_variant \
                    = os.path.join( constants.workspace
                                  , already_tested_program_folder
                                  , constants.symbooglix_output_directory
                                  , constants.symbooglix_terminated_states_directory
                                  , constants.constraint_solver_source_file)

                # specify input files.
                input_files \
                    = terminated_states_file_of_to_be_tested_variant + ' ' + terminated_states_of_already_tested_variant

                # specify output file.
                output_directory \
                    = os.path.join( constants.workspace
                                  , to_be_tested_program_folder
                                  , constants.constraint_solver_output_directory)

                # specify report file.
                report_file \
                    = os.path.join(constants.workspace
                                   , to_be_tested_program_folder
                                   , 'report.json')

                # build command for CONSTRAINT_SOLVER.
                cmd = [ 'ConstraintSolver.py'
                      , input_files
                      , '--compare-states'
                      , '--report ' + report_file
                      , '--target ' + output_directory]

                # start measuring comparison time
                start_time = time.time()

                # call CONSTRAINT_SOLVER.
                check_output(misc.to_command(cmd), shell=True)

                # store comparison time
                comparison_report[str(already_tested_program_folder) + "," + str(to_be_tested_program_folder) + ")"] \
                    = "{:.3f} seconds".format(time.time() - start_time)

                # specifying output file.
                output_file \
                    = os.path.join( constants.workspace
                                  , to_be_tested_program_folder
                                  , constants.constraint_solver_output_directory
                                  , already_tested_program_folder + '.yml')

                # store result's file path.
                destinations[to_be_tested_program_folder].append(output_file)

            # print progress.
            bar.progress()

    except CalledProcessError as e:

        # print ERROR message.
        bar.error()

        logging.error("ERROR: %s", e.output)

    else:

        # print DONE message.
        bar.done()

    # store analysis report.
    report.store("comparison_time", comparison_report)

    return destinations


def explore():
    # TODO: provide additional definition for command line option -e
    return 'undefined'