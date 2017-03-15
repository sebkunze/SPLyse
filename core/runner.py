import os, sys

from subprocess             import call

from core.utils             import constants, logger, misc
from core.utils.progressbar import ProgressBar

bar = ProgressBar()

def generate_terminated_states(entry_point): # TODO: Do some refactoring!
    size = len(os.listdir(constants.workspace))

    # setup progressbar's size.
    bar.setup(size)

    # print skeleton.
    bar.prefix()

    # browse all translated source files of the software product line variant.
    for folder in os.listdir(constants.workspace):
        # ignore MacOS' custom attributes of the analysed folder.
        if folder == '.DS_Store':
            continue

        # STEP 1: Merging all source files.
        logger.info('Start merging all translated source files in folder %s to symbooglix executeable', folder)
        for root, dirs, files in os.walk(os.path.join(constants.workspace, folder)):
            # write prefix for boogie heap abstraction.
            heap  = open(os.path.join(constants.java2boogie_home_environment, 'prefix', 'heap.bpl'))
            stack = open(os.path.join(constants.java2boogie_home_environment, 'prefix', 'stack.bpl'))
            test  = open(os.path.join(constants.java2boogie_home_environment, 'prefix', 'test.bpl'))
            code  = open(os.path.join(constants.java2boogie_home_environment, 'prefix', 'code.bpl'))

            # open boogie target file.
            target = open(os.path.join(root, constants.translated_file_name), 'a')

            target.write(heap.read())
            target.write(stack.read())
            target.write(test.read())
            target.write(code.read())

            for f in [f for f in files if not f == constants.translated_file_name]:
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
                if f == constants.translated_file_name:
                    source = os.path.join(root, f)

                    # TODO: Parse output directory better!

                    # build command for SYMBOOGLIX
                    cmd = [ constants.RUNNER
                          , source
                          , '-e ' + entry_point
                          , '--esi-show-constraints 1'
                          , '--esi-show-vars 1'
                          , '--write-smt2 0'
                          , '--max-depth 1000'
                          , '--output-dir ' + str(constants.workspace) + '/' + folder + '/' + constants.symbooglix_output_directory
                          , '--file-logging 1'
                          , '--log-terminated-state-info 1'
                          , '--log-non-terminated-state-info 0']

                    # call SYMBOOGLIX
                    call(misc.to_command(cmd), shell=True)
        logger.info('Done analyzing variant in folder %s', folder)

        # STEP 3: Combining all terminated states to one single file.
        logger.info("Start combining terminated symbooglix states in folder %s", folder)

        terminated_states \
            = os.path.join( constants.workspace
                          , folder
                          , constants.symbooglix_output_directory)

        for root, dirs, files in os.walk(terminated_states):
            # open terminated states file.
            target = open(os.path.join(root, constants.constraint_solver_source_file), 'a')

            for f in [f for f in files if not f == constants.constraint_solver_source_file]:
                # open terminated state file.
                source = open(os.path.join(root, f), 'r')

                # append YML header and terminated state.
                target.write(constants.terminated_state_header)
                target.write(source.read())

                # close terminated state files.
                source.close()

            # close terminated states file.
            target.close()

        logger.info("Done combining terminated symbooglix states in folder %s", folder)

        # print progress.
        bar.progress()

    # print done.
    bar.suffix()