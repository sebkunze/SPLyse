#!/usr/bin/env python
import os, sys

from subprocess     import call, check_call
from core.logger    import info

workspace  = os.path.join(os.getcwd(),'.workspace')

boogie_source_file = 'exec.bpl'

symbooglix_home_environment = os.environ['SYMBOOGLIX_HOME']
symbooglix_output_directory = 'symbooglix-out'

constraint_solver_source_file      = 'Symbooglix.TerminatedWithoutError.yml'
constraint_solver_output_directory = 'solver-out'

terminated_state_header = '---\n!!python/object:core.object.data.symbooglix.TerminatedSymbooglixState\n'


def main():
    if len(sys.argv) < 3:
        print "Please specify software product line's source folder and its entry point to be tested!"
        exit()

    # retrieve base path and entry point of software product line!
    base_path   = sys.argv[1]
    entry_point = sys.argv[2]

    # create subdirectory for workspace and it clean up if existing
    set_up_workspace()

    # translate JAVA source files to BOOGIE files
    translate_source_files(base_path)

    # generate terminated states of BOOGIE files using SYMBOOGLIX
    generate_terminated_states(workspace, entry_point)

    # analyse terminated states using Constrain Solver
    analyse_terminated_states(workspace)


def set_up_workspace():
    # create subdirectory.
    if not os.path.exists(workspace):
        os.makedirs(workspace, 0755)
    # clean up subdirectory.
    else:
        for root, dirs, files in os.walk(workspace, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

def translate_source_files(base_path):
    # browse all source folders of the software product line variants.
    source_folder = os.listdir(base_path)
    for folder in source_folder:
        # ignore MacOS' custom attributes within analysed folder.
        if folder == '.DS_Store':
            continue

        info('Processing all source files within folder %s', folder)

        # browse all source files of each software product line variant.
        for root, dirs, files in os.walk(os.path.join(base_path, folder)):
            # filter Java files.
            source_files = [f for f in files if '.java' in f]

            for f in source_files:
                info('Start translating source file %s', f)

                # specify source and target files for Java2Boogie.
                source = os.path.join(root, f)
                target = os.path.join(workspace, folder, f).replace('.java','.bpl')

                # create folder if non-existing.
                if not os.path.exists(os.path.join(workspace, folder)):
                    os.mkdir(os.path.join(workspace, folder), 0755)

                # call Java2Boogie parser with respective options.
                call(['Java2Boogie', '-s', source, '-t', target])

                info('Done translating source file %s', f)

def generate_terminated_states(source_files, entry_point): # TODO: Do some refactoring!
    # browse all translated source files of the software product line variant.
    for folder in os.listdir(source_files):
        # ignore MacOS' custom attributes of the analysed folder.
        if folder == '.DS_Store':
            continue

        # STEP 1: Merging all source files.
        info('Start merging all translated source files in folder %s to symbooglix executeable', folder)
        for root, dirs, files in os.walk(os.path.join(workspace, folder)):
            # write prefix for boogie heap abstraction.
            heap   = open(os.path.join(os.getcwd(), 'Java2Boogie', 'prefix', 'heap.bpl'))

            # open boogie target file.
            target = open(os.path.join(root, boogie_source_file), 'a')

            target.write(heap.read())

            for f in [f for f in files if not f == boogie_source_file]:
                # open boogie source file.
                source = open(os.path.join(root, f), 'r')

                # append boogie source file to target file.
                target.write(source.read())

                # close boogie source file.
                source.close()

            # close boogie target file.
            target.close()
        info('Done merging all translated source files in folder %s to symbooglix executeable', folder)

        # STEP 2: Executing SYMBOOGLIX.
        info('Start analysing variant in folder %s', folder)
        for root, dirs, files in os.walk(os.path.join(workspace, folder)):
            for f in files:
                if f == boogie_source_file:
                    source = os.path.join(root, f)

                    # build command for SYMBOOGLIX
                    cmd = ['mono ' + symbooglix_home_environment + '/Debug/sbx.exe ' + source,
                           '-e ' + entry_point,
                           ' --esi-show-constraints 1',
                           '--esi-show-vars 1',
                           '--write-smt2 0',
                           '--max-depth 1000',
                           '--output-dir .workspace/' + folder + '/' + symbooglix_output_directory,
                           '--file-logging 1',
                           '--log-terminated-state-info 1',
                           '--log-non-terminated-state-info 0']

                    # call SYMBOOGLIX
                    call(to_command(cmd), shell=True)
        info('Done analyzing variant in folder %s', folder)

        # STEP 3: Combining all terminated states to one single file.
        info("Start combining terminated symbooglix states in folder %s", folder)
        terminated_states = os.path.join(workspace, folder, symbooglix_output_directory)
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
        info("Done combining terminated symbooglix states in folder %s", folder)

def analyse_terminated_states(source_files):
    # browse all terminated states of the software product line variant.
    for folder_a in os.listdir(source_files):
        # create subdirectory.
        if not os.path.exists(os.path.join(workspace, folder_a, constraint_solver_output_directory)):
            os.makedirs(os.path.join(workspace, folder_a, constraint_solver_output_directory), 0755)

        # specify terminated states of software product line variant A.
        terminated_states_file_a = os.path.join(source_files, folder_a, symbooglix_output_directory, 'terminated_states', constraint_solver_source_file)
        for folder_b in [folder for folder in os.listdir(source_files) if not folder == folder_a]:
            # specify terminated states of software product line variant B.
            terminated_states_file_b = os.path.join(source_files, folder_b, symbooglix_output_directory, 'terminated_states', constraint_solver_source_file)

            # specifying input files.
            input_files  = terminated_states_file_a + ',' + terminated_states_file_b

            # specifying output files.
            output_files = os.path.join(workspace, folder_a, constraint_solver_output_directory, folder_a + '#' + folder_b + '.txt')

            # build command for CONSTRAINT_SOLVER.
            cmd = ['ConstraintSolver.py',
                   '--input-files=' + input_files,
                   '--output-file=' + output_files]

            # call CONSTRAINT_SOLVER.
            call(to_command(cmd), shell=True)

def to_command(cmd):
    return ' '.join(cmd)

if __name__ == '__main__':
    main()