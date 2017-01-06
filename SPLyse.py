#!/usr/bin/env python
import os, sys

from subprocess     import call
from core.logger    import info, debug

workspace  = os.path.join(os.getcwd(),'.workspace')
symbooglix = 'exec.bpl'

def main():
    if len(sys.argv) < 2:
        print "Please specify software product line's source folder!"
        exit()

    # retrieve base path of software product line!
    path = sys.argv[1]

    if not os.path.exists(workspace):
        os.makedirs(workspace, 0755)

    # browse all source folders of the software product line variants.
    source_folder = os.listdir(path)
    for folder in source_folder:
        # ignore MacOS' custom attributes of the analysed folder.
        if folder == '.DS_Store':
            continue

        info('Processing all source files within folder %s', folder)

        # browse all source files of each software product line variant.
        for root, dirs, files in os.walk(os.path.join(path, folder)):
            # filter Java files.
            source_files = [f for f in files if '.java' in f]

            for f in source_files:
                info('Translating source file %s', f)

                # specify source and target files for Java2Boogie.
                source = os.path.join(root, f)
                target = os.path.join(workspace, folder, f).replace('.java','.bpl')

                # create folder if non-existing.
                if not os.path.exists(os.path.join(workspace, folder)):
                    os.mkdir(os.path.join(workspace, folder), 0755)

                # call Java2Boogie parser with respective options.
                call(['Java2Boogie', '-s', source, '-t', target])

    # browse all translated files of each software product line variant.
    parsed_source_folders = os.listdir(workspace)
    for folder in parsed_source_folders:
        # ignore MacOS' custom attributes of the analysed folder.
        if folder == '.DS_Store':
            continue

        info('Merging all translated source files in folder %s', folder)

        for root, dirs, files in os.walk(os.path.join(workspace, folder)):
            for f in [f for f in files if not f == symbooglix]:
                # Append boogie source files.
                source = open(os.path.join(root, f),          'r')
                target = open(os.path.join(root, symbooglix), 'a')

                target.write(source.read())

    # run symbooglix on merged files.
    for folder in parsed_source_folders:
        for root, dirs, files in os.walk(os.path.join(workspace, folder)):
            for f in files:
                if f == symbooglix:
                    info('Analysing variant in folder %s', folder)

                    source = os.path.join(root, f)
                    call(['mono $SYMBOOGLIX_HOME/Debug/sbx.exe ' + source + ' --esi-show-constraints 1 --esi-show-vars 1 --write-smt2 0 --max-depth 1000 --output-dir out'], shell=True)

if __name__ == '__main__':
    main()