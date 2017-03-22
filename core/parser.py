import os

from subprocess             import check_output, STDOUT, CalledProcessError

from core.utils             import constants, logger
from core.utils.exception   import SPLyseException
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

            # create folder if non-existing.
            if not os.path.exists(os.path.join(constants.workspace, variant)):
                os.mkdir(os.path.join(constants.workspace, variant), 0755)

            # specify source files for Java2Boogie.
            sources = reduce(lambda x,y: x + ' ' + y , source_files, '')

            # specify target files for Java2Boogie.
            target = os.path.join(constants.workspace, variant, constants.translated_file_name)

            cmd = ' '.join(
                [ constants.PARSER
                , sources
                , '-t'
                , target])

            # call Java2Boogie parser with respective options.
            check_output(cmd, shell=True, stderr=STDOUT)

            logger.info('Translated files to target file %s', target)

            # print progress.
            progress_bar.progress()

    except CalledProcessError as e:
        # stop progress bar.
        progress_bar.error() # TODO: Rename error to something more general.

        # print error message.
        print e.output # TODO: This should not be here.

        # raise custom exception.
        raise SPLyseException("Java2Boogie failed!")
    else:
        # print done.
        progress_bar.done()