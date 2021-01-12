# Youtube-Playlist-Extractor
## Basic Overview
Do you have an ever-growing playlist on Youtube with hundreds (if not thousands) of your favorite songs and videos?
And have you ever wanted to write down all the songs and artists of these musical works?
With the Youtube Playlist Extractor, you can do all of that and more.
* Store information about your playlist on a CSV file or a MySQL database or both!
* Reorganise your list by artist, genre, or popularity (based on view counts)
* More features in development! Stay tuned!

## Getting Started
Open the command line / terminal and navigate to the root folder you wish to install. After that, type the following commands:
```
git clone https://github.com/LongPhan1912/Youtube-Playlist-Extractor.git Youtube-Playlist-Extractor
cd Youtube-Playlist-Extractor
```
Now, you can access the relevant files to run the program.
Notice that some files, such as the `client_secret.json` file, have some fields that need to be filled in such as `client_id`, `project_id`, and `client_secret` as they are specific to each Youtube account. In other words, these are pieces of information personal to you. 

To get the information for these missing fields, you would have to successful connect to the Youtube Data API:
* First, access https://console.developers.google.com to create a new project.
* Once you are done, go to the Dashboard and click "ENABLE APIS AND SERVICES". Search for "YouTube Data API v3" and enable it.
* Follow the guide on https://developers.google.com/youtube/v3/getting-started to create your own API key and OAuth 2.0 Client ID (for Desktop).
* Go back to https://console.developers.google.com and download the JSON for the Desktop Client ID credentials. Now, you can fill in the missing information in the `client_secret.json` file.

Next, make sure to read carefully through the `main-extractor.py` file to fill in your personal `api_key` and `channel_id`. Note that the `main()` function provides you with a list of playlist choices, so that you can edit the `playlist_id` corresponding to a playlist of your choosing.

After making all the aforementioned changes, go back to the terminal and download the required libraries:
```
pip3 install -r requirements.txt
```
Everything's all set! Let's run the program.
To extract your Youtube playlist to a CSV file, run:
```
python3 main-extractor.py
```
To convert this new CSV file into a MySQL database, follow the steps in the `csv-to-mysql.py` file. The `main()` function here also lets you customise many variables so that you can create new tables based on subcategories such as your favorite artist name or music genre. Once you have made your changes, run:
```
python3 csv-to-mysql.py
```
Congrats! You have now successfully extracted and stored your Youtube playlist in a quick and convenient way, using the Youtube API and MySQL.

## Plans for the future
1/ Add a small data visualisation to see the distribution of music genres or artists
2/ Upload a new, specialised playlist back onto Youtube / Spotify / Amazon Prime Music (when the api for Amazon's available); for example, a playlist full of my favorite Taylor Swift songs;
3/ Develop a web application
