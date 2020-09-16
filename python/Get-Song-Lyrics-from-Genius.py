#!python

echo "Get Songs Lyrics from Genius.com"

echo "Assign your Genius.com credentials and select your artist"

import lyricsgenius as genius
geniusCreds = "{Credentials}"
artist_name = "{Your Chosen Artist}"

#Connect your credentials and chosen artist to the genius object then test the first 5 songs
api = genius.Genius(geniusCreds)
artist = api.search_artist(artist_name, max_songs=5)

import os
os.getcwd()

echo "This will store all your artists’ lyrics and Genius song info in a json file in your current directory"
artist.save_lyrics()

echo "Open the json file"
import pandas as pd
Artist=pd.read_json("Lyrics_{ArtistName}.json")

echo "Check the file is structured how we expected it to be by looking at some of the data individually"
Artist['songs']
Artist['songs'][5]['lyrics']

echo "Extract relevant song data & Create an empty dictionary to store the songs & related data"
artist_dict = {}
def collectSongData(adic):
    dps = list()
    title = adic['title'] #song title
    url = adic['raw']['url'] #spotify url
    artist = adic['artist'] #artist name(s)
    song_id = adic['raw']['id'] #spotify id
    lyrics = adic['lyrics'] #song lyrics
    year = adic['year'] #release date
    upload_date = adic['raw']['description_annotation']['annotatable']['client_timestamps']['lyrics_updated_at'] #lyrics upload date
    annotations = adic['raw']['annotation_count'] #total no. of annotations
    descr = adic['raw']['description'] #song descriptions
    
    dps.append((title,url,artist,song_id,lyrics,year,upload_date,annotations,descr)) #append all to one tuple list
    artist_dict[title] = dps #assign list to song dictionary entry named after song title
    
collectSongData(Artist['songs'][5]) #check function works

echo "Pick a song and test your dictionary has it"
artist_dict['{chosen song}'][0][4]

echo "Store the data in a CSV file"
import csv
def updateCSV_file():
    upload_count = 0 #Set upload counter
    location = "{suitable_file_location}" #Pick file location
    print("input filename of song file, please add .csv")
    filename = input() #give your file a name
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file: #open a new csv file
        a = csv.writer(file, delimiter=',') #split by comma
        #(title,url,artist,song_id,lyrics,year,upload_date,annotations,descr)
        headers = ["Title","URL","Artist", "Song ID", "Lyrics", "Year", "Upload Date", "Annotations","Description"] #create header row
        a.writerow(headers) #add header row
        for song in artist_dict:
            a.writerow(artist_dict[song][0])
            upload_count+=1
            
        print(str(upload_count) + " songs have been uploaded")
updateCSV_file()

echo "Now your songs are in a CSV file you can perform further analysis however you like"
