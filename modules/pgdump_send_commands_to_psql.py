import psycopg2 #import connect, extensions, sql
from configparser import ConfigParser

def retrieve_config_parameters(filename, section):
    """
    Retrieves the config parameters that specify how to connect to a database.
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect_execute_disconnect_from_psql(filename, section, command_list, println = True):
    """ 
    Connects to the PostgreSQL database server using the config parameters available in
    <filename>, section <section>. Executes a list of SQL commands <command_list>. Then
    Exits.
    """
    # Variable initialization
    conn = None
    ##########
    try:
        # Reads connection parameters
        params = retrieve_config_parameters(filename, section)
        # connect to the PostgreSQL server
        if println: print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # get the isolation leve for autocommit
        autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        if println: print("ISOLATION_LEVEL_AUTOCOMMIT:", psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        # set the isolation level for the connection's cursors
        # will raise ActiveSqlTransaction exception otherwise
        conn.set_isolation_level( autocommit )
        # create a cursor
        cur = conn.cursor()
        # execute The statements
        for statement in command_list:
            try:
                if println: print(statement)
                cur.execute(command_list[statement])
            except Exception as error:
                print("Failed: " + str(error))
        # close the communication with the PostgreSQL
        try:
            record = cur.fetchall()
        except Exception as error:
            record = "No results to fetch"
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        record = "No results to fetch - error occured"
        print(error)
    finally:
        if conn is not None:
            conn.close()
            if println: print('Database connection closed.')
            return record
