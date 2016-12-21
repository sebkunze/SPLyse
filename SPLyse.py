#!/usr/bin/env python
import os, sys, logging

from subprocess import call

workspace = os.path.join(os.getcwd(),'.workspace')
symbooglix = 'symbooglix.bpl'

logging.basicConfig(filename='info.log',level=logging.INFO)

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
        logging.info('Processing all source files within folder %s', folder)

        # browse all source files of each software product line variant.
        for root, dirs, files in os.walk(os.path.join(path, folder)):
            for file in files:
                if '.java' in file:
                    logging.info('Translating source file %s', file)

                    source        = os.path.join(root, file)
                    target        = os.path.join(workspace, folder, file)

                    if not os.path.exists(os.path.join(workspace, folder)):
                        os.mkdir(os.path.join(workspace, folder), 0755)

                    # call Java2Boogie parser with respective options.
                    call(['Java2Boogie', '-s', source, '-t', target])

    # browse all translated files of each software product line variant.
    parsed_source_folders = os.listdir(workspace)
    for folder in parsed_source_folders:
        logging.info('Merging all translated source files in %s', folder)

        for root, dirs, files in os.walk(os.path.join(workspace, folder)):
            for file in files:
                # TODO: Find a more elegant version!
                if file.endswith('.bpl'):
                    continue

                source = open(os.path.join(root, file),       'r')
                target = open(os.path.join(root, symbooglix), 'a')

                target.write(source.read())

    # TODO: Set glaobal variable for symbooglix!
    # run symbooglix on given files
    # for folder in parsed_source_folders:
    #     for root, dirs, files in os.walk(os.path.join(workspace, folder)):
    #         if file == symbooglix:
    #             call([symbooglix, os.path.join(root, file)])

if __name__ == '__main__':
    main()