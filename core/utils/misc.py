import os

from core.utils import logger


def set_up_workspace(directory):
    # create subdirectory.
    if not os.path.exists(directory):
        os.makedirs(directory, 0755)
    # clean up subdirectory.
    else:
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def search_source_folder(directory):
    # browse directory.
    for root, dirs, _ in os.walk(directory, topdown=True):
        # check sub-directories.
        source_folder = [d for d in dirs if d == 'src-gen']
        if source_folder:
            return os.path.join(root, source_folder[0])


def search_test_folder(directory):
    # browse directory.
    for root, dirs, _ in os.walk(directory, topdown=True):
        # check folder's name.
        source_folder = [d for d in dirs if d == 'src-test']
        if source_folder:
            return os.path.join(root, source_folder[0])


def search_sources_files(directory, variant):
    sources = []

    logger.info("Searching source folder for variant %s.", variant)

    folder = search_source_folder(directory)
    for root, dirs, _ in os.walk(folder, topdown=False):
        variant_folder = [d for d in dirs if d == variant]
        if variant_folder:
            source_folder = os.path.join(root, variant_folder[0])

            logger.info("Found source folder at %s.", source_folder)

            sources.append(source_folder)

            break

    logger.info("Collecting source files%s.", '')

    source_files = []
    for source in sources:
        for root, dirs, files in os.walk(source, topdown=False):
            source_files += [os.path.join(root, f) for f in files if '.java' in f]

    logger.info("Collected source files %s.", source_files)

    return source_files


def look_up_source_files(directory, variants):
    sources = {}

    # searching each variants source files.
    for variant in variants:
        sources[variant] = search_sources_files(directory, variant)

    return sources

def search_test_files(directory, variant):
    sources = []

    logger.info("Searching test folder for variant %s.", variant)

    folder = search_test_folder(directory)
    for root, dirs, _ in os.walk(folder, topdown=False):
        variant_folder = [d for d in dirs if d == variant]
        if variant_folder:
            test_folder = os.path.join(root, variant_folder[0])

            logger.info("Found test folder at %s.", test_folder)

            sources.append(test_folder)

            break

    logger.info("Collecting source files%s.", '')

    source_files = []
    for source in sources:
        for root, dirs, files in os.walk(source, topdown=False):
            source_files += [os.path.join(root, f) for f in files if '.java' in f]

    logger.info("Collected source files %s.", source_files)

    return source_files

def look_up_test_files(directory, variants):
    tests = {}

    # searching each variants test files.
    for variant in variants:
        tests[variant] = search_test_files(directory, variant)

    return tests

def to_command(cmd):
    return ' '.join(cmd)