from .pgdump_send_commands_to_psql import connect_execute_disconnect_from_psql

def make_tuple_tags(tags):
    """
    Checks for tags, whether single or a list and return a string that can be used in
    a postgreSQL command. e.g.
    "tag1"        > "IN ('tag1')"
    "[tag1,tag2]" > "IN ('tag1','tag2')"
    """
    if type(tags) == str:
        return f"= {tags}"
    elif type(tags) == list:
        tup = "IN ("
        for tag in tags:
            tup += f"'{tag}',"
        tup = tup[:-1] + ")" 
        return tup
    else:
        return ""

def retrieve_tag_id(tags):
    """
    Retrieves the id of the tags. e.g.
    "safe" > "40482"
    """
    tags = make_tuple_tags(tags)
    if tags == "": return None
    command = {"retrieve tag id":f"SELECT id FROM new_tags WHERE name {tags};"}
    print(command)
    ids = connect_execute_disconnect_from_psql(filename="database.ini",
                                               section="restoring_derpi_lite",
                                               command_list=command,
                                               println = False)
    if type(ids) == list:
        return [i[0] for i in ids]
    else: 
        return ids

def create_dataset_csv(tags, sample_number, target_database_folder):
    """
    Retrieves a <sample_number> of entries (only their id and url) from the dataset which have the 
    affiliated <tags> tags. Saves the results in a .csv file in the <target_database_folder> path.
    """
    id_tags = retrieve_tag_id(tags)
    path = target_database_folder+"_".join(map(str,id_tags))
    command = {"create CSV":"COPY (SELECT id, image_format, version_path FROM new_images WHERE id IN (SELECT image_id FROM new_image_taggings" \
              f" WHERE tag_id {make_tuple_tags(id_tags)}) ORDER BY RANDOM() LIMIT {sample_number}) TO '{path}.csv' DELIMITER '|' CSV;"}
    print(command["create CSV"])
    connect_execute_disconnect_from_psql(filename="database.ini",
                                         section="restoring_derpi_lite",
                                         command_list=command,
                                         println = False)
    return path
