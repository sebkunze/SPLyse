import os

from subprocess import call

from core.utils import constants, logger, misc


boogie_file_extension = 'exec.bpl'

symbooglix_home_environment = os.environ['SYMBOOGLIX_HOME']
symbooglix_output_directory = 'symbooglix-out'

constraint_solver_source_file      = 'Symbooglix.TerminatedWithoutError.yml'
constraint_solver_output_directory = 'solver-out'

terminated_state_header = '---\n!!python/object:core.object.data.symbooglix.TerminatedSymbooglixState\n'


def generate_terminated_states(entry_point): # TODO: Do some refactoring!
    # browse all translated source files of the software product line variant.
    for folder in os.listdir(constants.workspace):
        # ignore MacOS' custom attributes of the analysed folder.
        if folder == '.DS_Store':
            continue

        # STEP 1: Merging all source files.
        logger.info('Start merging all translated source files in folder %s to symbooglix executeable', folder)
        for root, dirs, files in os.walk(os.path.join(constants.workspace, folder)):
            # write prefix for boogie heap abstraction.
            heap   = open(os.path.join(os.getcwd(), 'Java2Boogie', 'prefix', 'heap.bpl'))

            # open boogie target file.
            target = open(os.path.join(root, boogie_file_extension), 'a')

            target.write(heap.read())

            for f in [f for f in files if not f == boogie_file_extension]:
                # open boogie source file.
                source = open(os.path.join(root, f), 'r')

                # append boogie source file to target file.
                target.write(source.read())

                # close boogie source file.
                source.close()

            # close boogie target file.
            target.close()
        logger.info('Done merging all translated source files in folder %s to symbooglix executeable', folder)

        # STEP 2: Executing SYMBOOGLIX.
        logger.info('Start analysing variant in folder %s', folder)
        for root, dirs, files in os.walk(os.path.join(constants.workspace, folder)):
            for f in files:
                if f == boogie_file_extension:
                    source = os.path.join(root, f)

                    # build command for SYMBOOGLIX
                    cmd = ['mono ' + symbooglix_home_environment + '/Debug/sbx.exe ' + source,
                           '-e ' + entry_point,
                           '--esi-show-constraints 1',
                           '--esi-show-vars 1',
                           '--write-smt2 0',
                           '--max-depth 1000',
                           '--output-dir .workspace/' + folder + '/' + symbooglix_output_directory,
                           '--file-logging 1',
                           '--log-terminated-state-info 1',
                           '--log-non-terminated-state-info 0']

                    # call SYMBOOGLIX
                    call(misc.to_command(cmd), shell=True)
        logger.info('Done analyzing variant in folder %s', folder)

        # STEP 3: Combining all terminated states to one single file.
        logger.info("Start combining terminated symbooglix states in folder %s", folder)
        terminated_states = os.path.join(constants.workspace, folder, symbooglix_output_directory)
        for root, dirs, files in os.walk(terminated_states):
            # open terminated states file.
            target = open(os.path.join(root, constraint_solver_source_file), 'a')

            for f in [f for f in files if not f == constraint_solver_source_file]:
                # open terminated state file.
                source = open(os.path.join(root, f), 'r')

                # append YML header and terminated state.
                target.write(terminated_state_header)
                target.write(source.read())

                # close terminated state files.
                source.close()

            # close terminated states file.
            target.close()
        logger.info("Done combining terminated symbooglix states in folder %s", folder)