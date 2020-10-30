from .pgdump_send_commands_to_psql import retrieve_config_parameters
import subprocess, os
import shlex 

def export_tables_to_db(filename, section, db_source, db_target, table_to_move):
    """
    Restores a postgreSQL database from a pgdump file.
    """
    # Reads connection parameters
    parameters = retrieve_config_parameters(filename, section)
    # Stores connection parameters into variables
    DB_USER = parameters["user"]
    DB_PORT = parameters["port"]
    DB_PASSWORD = parameters["password"]
    # Sets the environment to register the password to the DB
    my_env = os.environ
    my_env["PGPASSWORD"] = DB_PASSWORD
    print (f"Moving {table_to_move} from {db_source} to {db_target} -- Please wait")
    # Performs the restore via a subprocess command
    command_for_dumping = f'pg_dump -U {DB_USER} ' \
                f'-t {table_to_move} ' \
                f'{db_source} | psql ' \
                f'-p {DB_PORT} ' \
                f'-U {DB_USER} ' \
                f'-W {db_target} '
    print(command_for_dumping)
    proc = subprocess.Popen(shlex.split(command_for_dumping), 
                            bufsize=1, 
                            shell=True, 
                            universal_newlines=True, 
                            env=my_env)
    proc.poll()
    print ("Move in Process")
