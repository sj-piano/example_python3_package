# Imports
import os
import sys
import argparse
import logging




# Local imports
# (Can't use relative imports because this is a top-level script)
import example_python3_package




# Shortcuts
from os.path import isdir, isfile, join
util = example_python3_package.util
v = util.validate




# Set up logger for this module. By default, it produces no output.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.ERROR)
log = logger.info
deb = logger.debug




def setup(
    log_level = 'error',
    debug = False,
    log_timestamp = False,
    log_file = None,
    ):
  logger_name = 'cli'
  # Configure logger for this module.
  example_python3_package.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = logger_name,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )
  deb('Setup complete.')
  # Configure logging levels for example_python3_package package.
  # By default, without setup, it logs at ERROR level.
  # Optionally, the package could be configured here to use a different log level, by e.g. passing in 'error' instead of log_level.
  example_python3_package.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_file = log_file,
  )




def main():

  # Capture and parse command-line arguments.

  # Note: We use camelCase for option names because it's faster to type.

  parser = argparse.ArgumentParser(
    description='Command-Line Interface (CLI) for using the example_python3_package package.'
  )

  parser.add_argument(
    '-t', '--task',
    help="Task to perform (default: '%(default)s').",
    default='hello',
  )

  parser.add_argument(
    '-l', '--logLevel', type=str, dest='log_level',
    choices=['debug', 'info', 'warning', 'error'],
    help="Choose logging level (default: '%(default)s').",
    default='error',
  )

  parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help="Sets logLevel to 'debug'. This overrides --logLevel.",
  )

  parser.add_argument(
    '-s', '--logTimestamp', dest='log_timestamp',
    action='store_true',
    help="Choose whether to prepend a timestamp to each log line.",
  )

  parser.add_argument(
    '-x', '--logToFile', dest='log_to_file',
    action='store_true',
    help="Choose whether to save log output to a file.",
  )

  parser.add_argument(
    '-z', '--logFile', dest='log_file',
    help="The path to the file that log output will be written to.",
    default='log_example_python3_package.txt',
  )

  a = parser.parse_args()

  # Check and analyse arguments
  if not a.log_to_file:
    a.log_file = None

  # Setup
  setup(
    log_level = a.log_level,
    debug = a.debug,
    log_timestamp = a.log_timestamp,
    log_file = a.log_file,
  )

  # Note: If you add a new task function, then its name must be added to this list.
  tasks = """
hello hello2 hello3
getPythonVersion
""".split()
  if a.task not in tasks:
    msg = "Unrecognised task: {}".format(a.task)
    msg += "\nTask list: {}".format(tasks)
    stop(msg)

  # Run top-level function (i.e. the appropriate task).
  globals()[a.task](a)




def hello(a):
  # Confirm:
  # - that we can run a simple task.
  # - that this tool has working logging.
  log('Log statement at INFO level')
  deb('Log statement at DEBUG level')
  print('hello world')




def hello2(a):
  # Confirm:
  # - that we can run a simple task from within the package.
  # - that the package has working logging.
  example_python3_package.code.hello.hello()




def hello3(a):
  # Confirm:
  # - that we can run a simple package task that loads a resource file that is stored with the code.
  example_python3_package.code.hello.hello_resource()




def getPythonVersion(a):
  # Confirm:
  # - that we can run a shell command.
  check = util.misc.shell_tool_exists('python3')
  v.validate_boolean(check)
  if not check == True:
    msg = "Can't find 'python3' tool in bash shell'"
    raise ValueError(msg)
  cmd = 'python3 --version'
  output, exit_code = util.misc.run_local_cmd(cmd)
  if exit_code != 0:
    msg = "Ran command = '{x}', but got exit code = {c}".format(x=cmd, c=exit_code)
    raise ValueError(msg)
  print(output.strip())




def stop(msg=None):
  if msg is not None:
    print(msg)
  import sys
  sys.exit()




if __name__ == '__main__':
  main()
