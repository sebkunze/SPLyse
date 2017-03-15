import os, sys

from collections            import defaultdict
from subprocess             import call

from core.utils             import constants, logger, misc
from core.utils.progressbar import ProgressBar


bar = ProgressBar()


def analyse():
    size = len(os.listdir(constants.workspace))

    # setup progressbar's size.
    bar.setup(size)

    # print skeleton.
    bar.prefix()

    # browse all terminated states of the software product line variant.
    for to_be_analysed_program_folder in os.listdir(constants.workspace):
        subdirectory \
            = os.path.join( constants.workspace
                          , to_be_analysed_program_folder
                          , constants.constraint_solver_output_directory)

        # create subdirectory.
        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory, 0755)

        # specifying output file.
        input_files \
            = os.path.join( constants.workspace
                          , to_be_analysed_program_folder
                          , constants.symbooglix_output_directory
                          , 'terminated_states'
                          , constants.constraint_solver_source_file)

        # specifying output file.
        output_files \
            = os.path.join( constants.workspace
                          , to_be_analysed_program_folder
                          , constants.constraint_solver_output_directory
                          , constants.analysed_file_name)

        # build command for CONSTRAINT_SOLVER.
        cmd = ['ConstraintSolver.py',
                input_files,
                '--analyse-states',
                '--target ' + output_files]

        # call CONSTRAINT_SOLVER.
        call(misc.to_command(cmd), shell=True)

        # print progress.
        bar.progress()

    # print done.
    bar.suffix()


def compare():
    number_of_variant_directories = len(os.listdir(constants.workspace))

    if number_of_variant_directories == 1:
        print ""
        print "> ERROR: TOO FEW VARIANTS FOR COMPARISON."
        return

    size \
        = len(os.listdir(constants.workspace))

    # setup progressbar's size.
    bar.setup(size)

    # print skeleton.
    bar.prefix()

    # declare dictionary storing results' file path.
    destinations = defaultdict(list)

    # browse all terminated states of the software product line variant.
    for to_be_tested_program_folder in os.listdir(constants.workspace):
        subdirectory \
            = os.path.join( constants.workspace
                          , to_be_tested_program_folder
                          , constants.constraint_solver_output_directory)

        # create subdirectory.
        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory, 0755)

        # specify terminated states of software product line variant A.
        terminated_states_file_a \
            = os.path.join( constants.workspace
                          , to_be_tested_program_folder
                          , constants.symbooglix_output_directory
                          , constants.symbooglix_terminated_states_directory
                          , constants.constraint_solver_source_file)

        # collect folders of already tested programs.
        already_tested_program_folders \
            = [folder for folder in os.listdir(constants.workspace) if not folder == to_be_tested_program_folder]

        for already_tested_program_folder in already_tested_program_folders:
            # specify terminated states of software product line variant B.
            terminated_states_file_b \
                = os.path.join( constants.workspace
                              , already_tested_program_folder
                              , constants.symbooglix_output_directory
                              , constants.symbooglix_terminated_states_directory
                              , constants.constraint_solver_source_file)

            # specifying input files.
            input_files = terminated_states_file_a + ' ' + terminated_states_file_b

            # specifying output files.
            output_files \
                = os.path.join( constants.workspace
                              , to_be_tested_program_folder
                              , constants.constraint_solver_output_directory
                              , already_tested_program_folder + '.yml')

            # build command for CONSTRAINT_SOLVER.
            cmd = [ 'ConstraintSolver.py'
                  , input_files
                  , '--compare-states'
                  , '--target ' + output_files]

            # call CONSTRAINT_SOLVER.
            call(misc.to_command(cmd), shell=True)

            # store result's file path.
            destinations[to_be_tested_program_folder].append(output_files)

        # print progress.
        bar.progress()

    # print done.
    bar.suffix()

    return destinations


def explore():
    return 'undefined'