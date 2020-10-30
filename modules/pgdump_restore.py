from .pgdump_send_commands_to_psql import retrieve_config_parameters
import subprocess, os
import shlex 

def restore_db(filename, section, source, target_folder):
    """
    Restores a postgreSQL database from a pgdump file.
    """
    # Reads connection parameters
    parameters = retrieve_config_parameters(filename, section)
    # Stores connection parameters into variables
    DB_NAME = parameters["database"]
    DB_SOURCE = target_folder + source
    DB_USER = parameters["user"]
    DB_HOST = parameters["host"]
    DB_PORT = parameters["port"]
    DB_PASSWORD = parameters["password"]
    # Sets the environment to register the password to the DB
    my_env = os.environ
    my_env["PGPASSWORD"] = DB_PASSWORD
    print (f"Restoring {DB_NAME} -- Please wait")
    # Performs the restore via a subprocess command
    command_for_dumping = f"pg_restore -v -O -h {DB_HOST} " \
                f"-p {DB_PORT} " \
                f"-U {DB_USER} " \
                f"-d {DB_NAME} " \
                f"{DB_SOURCE} "
    proc = subprocess.Popen(shlex.split(command_for_dumping), 
                            bufsize=1, 
                            shell=True, 
                            universal_newlines=True, 
                            env=my_env)
    proc.poll()
    print (f"Restoration of {DB_NAME} in process")
    print("This might take up to an hour on an hdd, " \
          "please be patient and use psql to check process")

