import os

from subprocess import call

from core.utils  import constants, logger, misc


def analyse():
    counter = 1;
    number = 1 if len(os.listdir(constants.workspace)) is 1 else len(os.listdir(constants.workspace)) * (len(os.listdir(constants.workspace)) - 1)

    # browse all terminated states of the software product line variant.
    for folder in os.listdir(constants.workspace):
        # create subdirectory.
        if not os.path.exists(os.path.join(constants.workspace, folder, constants.constraint_solver_output_directory)):
            os.makedirs(os.path.join(constants.workspace, folder, constants.constraint_solver_output_directory), 0755)

        # specifying output file.
        input_files = os.path.join(constants.workspace, folder, constants.symbooglix_output_directory, 'terminated_states', constants.constraint_solver_source_file)

        # specifying output file.
        output_files = os.path.join(constants.workspace, folder, constants.constraint_solver_output_directory, folder + '.yml')

        print "- analysing variant " + str(counter) + " of " + str(number)
        counter+=1

        # build command for CONSTRAINT_SOLVER.
        cmd = ['ConstraintSolver.py',
                input_files,
                '--analyse-states',
                '--target ' + output_files]

        # call CONSTRAINT_SOLVER.
        call(misc.to_command(cmd), shell=True)


def guide():
    if len(os.listdir(constants.workspace)) == 1:
        print "- too few variants for comparison."
        return

    counter = 1;
    number = len(os.listdir(constants.workspace)) * (len(os.listdir(constants.workspace)) - 1)
    # browse all terminated states of the software product line variant.
    for folder_a in os.listdir(constants.workspace):
        # create subdirectory.
        if not os.path.exists(os.path.join(constants.workspace, folder_a, constants.constraint_solver_output_directory)):
            os.makedirs(os.path.join(constants.workspace, folder_a, constants.constraint_solver_output_directory), 0755)

        # specify terminated states of software product line variant A.
        terminated_states_file_a = os.path.join(constants.workspace, folder_a, constants.symbooglix_output_directory, 'terminated_states', constants.constraint_solver_source_file)
        for folder_b in [folder for folder in os.listdir(constants.workspace) if not folder == folder_a]:
            # specify terminated states of software product line variant B.
            terminated_states_file_b = os.path.join(constants.workspace, folder_b, constants.symbooglix_output_directory, 'terminated_states', constants.constraint_solver_source_file)

            # specifying input files.
            input_files = terminated_states_file_a + ' ' + terminated_states_file_b

            # specifying output files.
            output_files = os.path.join(constants.workspace, folder_a, constants.constraint_solver_output_directory, folder_a + '#' + folder_b + '.yml')

            print "- comparing variant combination " + str(counter) + " of " + str(number)
            counter+=1

            # build command for CONSTRAINT_SOLVER.
            cmd = ['ConstraintSolver.py',
                   input_files,
                   '--compare-states',
                   '--target ' + output_files]

            # call CONSTRAINT_SOLVER.
            call(misc.to_command(cmd), shell=True)