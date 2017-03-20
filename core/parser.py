import os, sys

from subprocess             import check_output, STDOUT, CalledProcessError

from core.utils             import constants, logger, misc
from core.utils.progressbar import ProgressBar


progress_bar = ProgressBar()


def translate_source_files(sources):
    size = len(sources.items())

    # setup progressbar's size.
    progress_bar.setup(size)

    # print skeleton.
    progress_bar.bar()

    try:
        for variant, source_files in sources.items():
            logger.info('Translating files for variant %s', variant)

            for source_file in source_files:
                # extract name of source file.
                name = source_file.split('/')[-1].replace('.java', '.bpl')

                # specify target files for Java2Boogie.
                target_file = os.path.join(constants.workspace, variant, name)

                # create folder if non-existing.
                if not os.path.exists(os.path.join(constants.workspace, variant)):
                    os.mkdir(os.path.join(constants.workspace, variant), 0755)

                logger.info('- From source file %s', source_file)

                cmd = [ 'Java2Boogie'
                       , '-s'
                       , source_file
                       , '-t'
                       , target_file]

                # call Java2Boogie parser with respective options.
                check_output(misc.to_command(cmd), shell=True, stderr=STDOUT)

                logger.info('- To   target file %s', target_file)

            # print progress.
            progress_bar.progress()

    except CalledProcessError as e:
        progress_bar.error()

        print e.output
    else:
        # print done.
        progress_bar.done()