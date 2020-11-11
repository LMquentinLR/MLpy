from .pgdump_send_commands_to_psql import retrieve_config_parameters
import subprocess, os
import shlex 
from datetime import date

def save_db(filename, section, filename_of_db, target_folder):
    """
    Saves a postgreSQL database into a .pgdump file.
    """
    # Reads connection parameters
    parameters = retrieve_config_parameters(filename, section)
    # Stores connection parameters into variables
    DB_USER = parameters["user"]
    DB_PASSWORD = parameters["password"]
    date_save =  "{:%Y_%m_%d}".format(date.today())
    # Sets the environment to register the password to the DB
    my_env = os.environ
    my_env["PGPASSWORD"] = DB_PASSWORD
    print (f"Saving {filename_of_db} -- Please wait")
    # Performs the restore via a subprocess command
    command_for_dumping = f"pg_dump -U {DB_USER} " \
                f"-Fc {filename_of_db} > " \
                f"{target_folder+filename_of_db}_{date_save}.pgdump"
    proc = subprocess.Popen(shlex.split(command_for_dumping), 
                            bufsize=1, 
                            shell=True, 
                            universal_newlines=True, 
                            env=my_env)
    proc.poll()
    print (f"Saving in process")
    print("This might take, please be patient and use psql to check process")
