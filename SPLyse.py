#!/usr/bin/env python
import os, sys

from subprocess import call
from core.logger import info

workspace = os.path.join(os.getcwd(),'.workspace')

def main():
    if len(sys.argv) < 2:
        print "Please specify software product line's source folder!"
        exit()

    # retrieve base path of software product line!
    path = sys.argv[1]

    if not os.path.exists(workspace): # TODO: Clear workspace!
        os.makedirs(workspace, 0755)

    # browse all source folders of the software product line variants.
    source_folders = os.listdir(path)
    for folder in source_folders:
        info('Processing all source files within folder %s', folder)

        # browse all source files of each software product line variant.
        for root, dirs, files in os.walk(os.path.join(path, folder)):
            for file in files:
                if '.java' in file:
                    info('Translating source file %s', file)

                    source = os.path.join(root, file)
                    # TODO: Find more readable implementation!
                    target = os.path.join(workspace, folder, file).replace('.java','.bpl')

                    if not os.path.exists(os.path.join(workspace, folder)):
                        os.mkdir(os.path.join(workspace, folder), 0755)

                    # Call Java2Boogie parser with respective options.
                    call(['Java2Boogie', '-s', source, '-t', target])

    # browse all translated files of each software product line variant.
    parsed_source_folders = os.listdir(workspace)
    for folder in parsed_source_folders:
        info('Merging all translated source files in %s', folder)

        for root, dirs, files in os.walk(os.path.join(workspace, folder)):

            # Build the name for boogie source file, i.e., the software product line variant's name.
            name = os.path.split(root)[-1] + '.bpl'

            for file in [f for f in files if not f == name]:

                # Append boogie source files.
                source = open(os.path.join(root, file), 'r')
                target = open(os.path.join(root, name), 'a')

                target.write(source.read())

    # TODO: Set glaobal variable for symbooglix!
    # run symbooglix on given files
    # for folder in parsed_source_folders:
    #     for root, dirs, files in os.walk(os.path.join(workspace, folder)):
    #         if file == symbooglix:
    #             call([symbooglix, os.path.join(root, file)])

if __name__ == '__main__':
    main()