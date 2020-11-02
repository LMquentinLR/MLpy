import urllib.request
from urllib.error import HTTPError
import csv
import time
from .pgdump_send_commands_to_psql import retrieve_config_parameters
import os

def download_images(target_database_folder, path_class):
    """
    Downloads the images referenced in a csv file located at <path_class.csv>
    Saves the images in <target_database_folder + path_class.split("/")[-1] + "/"> with for name their id.
    """
    folder_path = target_database_folder + path_class.split("/")[-1] + "/"
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    
    API_key = retrieve_config_parameters("database.ini", "derpibooru_API_key")
    API_key = API_key["password"]
    
    error = 0
    
    # Opens the reference csv file that contains the images' id, format and url
    with open(path_class + ".csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        # For each image:
        for idx, row in enumerate(reader):
            # Constructs the image's url
            filename, ext, url = row[0].split("|")
            full_url = url + "medium." + ext.lower() + f"?key={API_key}"
            # Requests the image from derpibooru
            try:
                r = urllib.request.urlopen(full_url)
                # Saves the image
                with open(folder_path + f"{filename}." + ext, "wb") as f:
                    f.write(r.read())
            # in case of HTTP error, records the error and backs off for 5 seconds, goes to the next picture
            except HTTPError as e:
                with open(path_class + "_error.csv", "a", newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([f"{e} | {full_url}"])
                error += 1
                time.sleep(5)
            # in case of other error, records the error and backs off for one minute, goes to the next picture
            except Exception as e:
                with open(path_class + "_error.csv", "a", newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([f"{e} | {full_url}"])
                error += 1
                time.sleep(60)
            # Pauses for 1 second
            time.sleep(1)
            if (idx+1) % 100 == 0:
                print(f"#{idx+1} sent - #{idx-error+1} image downloaded - #{error} errors caught so far.")
    print(f"#{idx+1} sent - #{idx-error+1} image downloaded - #{error} errors caught so far.")
