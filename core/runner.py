import os
import logging

from subprocess             import check_output, call, CalledProcessError, STDOUT

from core.utils             import constants, misc
from core.utils.exception   import SPLyseException
from core.utils.progressbar import ProgressBar

# get logging instance.
log = logging.getLogger('SPLyse')

# get progress bar instance.
bar = ProgressBar()

def generate_terminated_states(entry_point): # TODO: Do some refactoring!
    size = len(os.listdir(constants.workspace))

    # setup progressbar's size.
    bar.setup(size)

    # print skeleton.
    bar.skeleton()

    # try:
    # browse all translated source files of the software product line variant.
    for folder in os.listdir(constants.workspace):
        # ignore MacOS' custom attributes of the analysed folder.
        if folder == '.DS_Store':
            continue

        # STEP 1: Executing SYMBOOGLIX.
        log.info('Start analysing variant in folder %s', folder)
        for root, dirs, files in os.walk(os.path.join(constants.workspace, folder)):
            for f in files:
                if f == constants.translated_file_name:
                    source = os.path.join(root, f)

                    log.debug("> Executing source file: %s", source)

                    target = str(constants.workspace) + '/' + folder + '/' + constants.symbooglix_output_directory

                    # build command for SYMBOOGLIX
                    cmd = [ constants.RUNNER
                          , source
                          , '-e ' + entry_point
                          , '--check-entry-requires 1'
                          , '--check-entry-axioms 1'
                          , '--esi-show-constraints 1'
                          , '--esi-show-vars 1'
                          , '--write-smt2 0'
                          , '--max-depth 1000'
                          , '--output-dir ' + target
                          , '--file-logging 1'
                          , '--log-terminated-state-info 1'
                          , '--log-non-terminated-state-info 0']

                    try:
                        # call SYMBOOGLIX
                        check_output(misc.to_command(cmd), shell=True)

                    except CalledProcessError as e:
                         # FIXME: SYMBOOGLIX returns ERRORS_NO_TIMEOUT even if executed with a valid program.
                        if e.returncode == 2:
                            continue
                        else:
                            raise SPLyseException("SYMBOOGLIX failed.")


        log.info('Done analyzing variant in folder %s', folder)

        # STEP 2: Combining all terminated states to one single file.
        log.info("Start combining terminated symbooglix states in folder %s", folder)

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

        log.info("Done combining terminated symbooglix states in folder %s", folder)

        # print progress.
        bar.progress()

    # print done.
    bar.done()