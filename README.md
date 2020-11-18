# MLpy

### What is it about?

> "Moderating on Discord is _hard_."
>
> **t**. _A lot of moderators_

Any moderation team on a Discord server can tell you that. Trolls, spammers, and all the highjinks involved in moderating hundred if not thousand of people is taxing. It is a day-long, year-round issue. Therefore the question outlined here is: Can this heavy process be helped?

The idea we will be interested in is dual: Can we build an image classification model, can a discord bot leverage that model for any purposes (here: moderating user posts). As such, this project will be about:

1. Improving our programming skills

2. Learning about Relational Databases

3. Teaching ourselves some advanced machine learning techniques

4. Building a proof-of-work chatroom bot that can read and evaluated pictures posted by users for a specific pupose (e.g. verifying if those pictures follow Discord's Terms of Service)

### Repository organization

To review the content, please follow the following notebook in a didactic way.

> 0_summary.ipynb
>
> 1_building_the_db_using_postgreSQL.ipynb
>
> 2_building_a_working_dataset.ipynb
> 
> 3_modeling.ipynb
> 
> 4_testing.ipynb


### Repository organization

```
MLpy
│   0_summary.ipynb
│   1_building_the_db_using_postgreSQL.ipynb
│   2_building_a_working_dataset.ipynb
│   3_modeling.ipynb
│   4_testing.ipynb
│   README.md
│   database.ini (not included but necessary)
│   database_example.ini
│   LICENSE
│   other_kept_models.zip
│   selected_model.h5
│   test_results_2020_11_11.csv
│
└───archive
│   │   1_manual_load_database.ipynb
│   │   3_modeling-archive.ipynb
│   │   MLpy_v1.ipynb
│   │   pgdump_full_to_lite.py
│   
└───bot_proof_of_concept
│   │   LICENSE
│   │   main.py
│   │   README.md
│   │   requirements.txt
│   │   setup.py
│   │
│   └───local_commands
│   │   │   __init__.py
│   │   │   commands.py
│   │
│   └───models
│       │   selected_model.h5
│   
└───data_dump
│   │
│   └───datasets
│       │
│       └───ds_test
│           │   39068_29300_26707.csv
│           │   39068_29300_26707_error.csv
│           │   40482.csv
│           │   40482_error.csv
│           │
│           └───test_data
│               │   39068_29300_26707.csv
│               │   39068_29300_26707_error.csv
│               │   40482.csv
│               │   40482_error.csv
│   
└───modules
│   │   __init__.py
│   │   download_dump.py
│   │   download_images.py
│   │   make_csv.py
│   │   model.py
│   │   pgdump_restore.py
│   │   pgdump_save_db.py
│   │   pgdump_send_commands_to_psql.py
│   
└───pictures
│   │   bot_app_1.PNG
│   │   bot_app_2.PNG
│   │   bot_app_3.PNG
│   │   bot_app_4.PNG
│   │   bot_app_5.PNG
│   │   bot_app_6.PNG
│   │   bot_app_7.PNG
│   │   derpibooru_db1.PNG
│   │   derpibooru_db2.PNG
│   │   derpibooru_db3.PNG
│   │   downloadPictureFailureRate.PNG
│   │   meme.PNG
│   │   model.png
│   │   modelParameters.PNG
│   │   test_example_1.jpg
│   │   test_example_2.jpg

```

### Disclaimer

Derpibooru's REST API license forbids a high load of requests per second, please keep the exponential back off functional if you try this code