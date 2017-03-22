import os

# -----------------------------------------------
#                  WORKSPACES
# -----------------------------------------------


workspace = os.path.join(os.getcwd(),'.SPLyse')


# -----------------------------------------------
#                PATH VARIABLES
# -----------------------------------------------


java2boogie_home_environment \
    = os.environ['JAVA2BOOGIE_HOME']

symbooglix_home_environment \
    = os.environ["SYMBOOGLIX_HOME"]


# -----------------------------------------------
#               TERMINAL COMMANDS
# -----------------------------------------------


OPTIMISER \
    = "JavaTestModifier"

PARSER \
    = "Java2Boogie.py"

RUNNER \
    = 'mono ' + symbooglix_home_environment + '/Debug/sbx.exe '

SOLVER \
    = "ConstraintSolver"

# -----------------------------------------------
#                   EXTERNAL
# -----------------------------------------------


symbooglix_output_directory \
    = "symbooglix-out"

symbooglix_terminated_states_directory \
    = "terminated_states"

symbooglix_terminated_state_file_name \
    = "Symbooglix.TerminatedWithoutError.yml"

constraint_solver_output_directory \
    = "solver-out"

constraint_solver_source_file \
    = "Symbooglix.TerminatedWithoutError.yml"


# -----------------------------------------------
#                   INTERNAL
# -----------------------------------------------


analysed_file_name = "analysis.yml"

translated_file_name = "exec.bpl"

terminated_state_header = '---\n!!python/object:core.object.data.symbooglix.TerminatedSymbooglixState\n'