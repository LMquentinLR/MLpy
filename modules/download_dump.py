import urllib
from pathlib import Path
from datetime import date, timedelta

def download_most_recent_pgdump(path):
    """
    Downloads the most recent .pg_dump from the derpibooru website into a folder <path>.
    """
    # Variable Initialization
    attempt = 0
    date_to_check = date.today()     
    source = "https://data.derpicdn.net/file/derpibooru-data/"
    ###########
    # Attempts to download a pgdump file with a maximum of 10 attempts
    while attempt < 10:
        # Increments the variable <attempt>
        attempt += 1
        # Creates a printable version of the date to be checked
        dt = "{:%Y_%m_%d}".format(date_to_check)
        # Try/Catch
        try:
            print("attempt " + str(attempt) + ": requesting pgdump for date " + dt)
            filename = "derpibooru_public_dump_" + dt + ".pgdump"
            if Path(path+filename).is_file():
                print("the pgdump " + filename + " is already available locally.")
                urllib.request.urlcleanup()
                return None
            urllib.request.urlretrieve(source + filename,
                                       path + filename)
            print("pgdump for date " + dt + " was downloaded")
            # Clean-up of the urllib cache if a pgdump was downloaded
            urllib.request.urlcleanup()
            return None
        except Exception as e:
            print(str(e) + " request failed for date " + dt)
        # Increments down the date to check if no dump was retrieved
        date_to_check -= timedelta(days=1)
    ###########
    # Clean-up of the urllib cache if no pgdump was downloaded
    print("Maximum number of attempts reached. No pgdump was downloaded")
    urllib.request.urlcleanup()
    return None
