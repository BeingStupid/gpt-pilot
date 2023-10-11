from __future__ import print_function, unicode_literals
import os
import sys
import traceback
from dotenv import load_dotenv
from utils.style import red
from utils.custom_print import get_custom_print
from helpers.Project import Project
from utils.arguments import get_arguments
from utils.exit import exit_gpt_pilot
from logger.logger import logger
from database import (
    database_exists,
    create_database,
    tables_exist,
    create_tables,
    get_created_apps_with_steps,
)

def init():
    load_dotenv()

    # Check if the "euclid" database exists, if not, create it
    if not database_exists():
        create_database()

    # Check if the tables exist, if not, create them
    if not tables_exist():
        create_tables()

    arguments = get_arguments()

    logger.info('Starting with args: %s', arguments)

    return arguments

if __name__ == "__main__":
    ask_feedback = True
    try:
        # Initialization and argument parsing
        args = init()
        builtins.print, ipc_client_instance = get_custom_print(args)

        if '--api-key' in args:
            os.environ["OPENAI_API_KEY"] = args['--api-key']

        if '--get-created-apps-with-steps' in args:
            print({ 'db_data': get_created_apps_with_steps() }, type='info')
        elif '--ux-test' in args:
            from test.ux_tests import run_test
            run_test(args['--ux-test'], args)
        else:
            # TODO: Project handling
            project = Project(args, ipc_client_instance=ipc_client_instance)
            project.start()
            # TODO: Handle project completion and user interactions
    except Exception as e:
        logger.error('GPT PILOT EXITING WITH ERROR')
        logger.exception(e)
        ask_feedback = False
    finally:
        exit_gpt_pilot(ask_feedback)
        sys.exit(0)
