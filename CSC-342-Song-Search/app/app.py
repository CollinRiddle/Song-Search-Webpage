from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

with open("top_tracks_2023.json") as f:
    data = json.load(f)

#Take in given song, return it's popularity value
def sort_by_popularity(song):
    return song["popularity"]

#Take in a given song, return its duration_mins value
def sort_by_duration(song):
    return song["duration_mins"]

@app.route("/search", methods=["GET"])
def search():
    #Obtain given searc query, default to none, same concept with obtaining other values below
    #with some basic parameters to default to.
    search_query = request.args.get("query", "").lower()
    search_by = request.args.get("search_by", "title")
    sort_by = request.args.get("sort_by", "popularity")
    explicit_param = request.args.get("explicit", "false")
    
    if explicit_param.lower() == "true":
        include_explicit = True
    else:
        include_explicit = False

    # Create an empty list to store filtered songs
    filtered_songs = []

    for song in data:
        # Check if the song matches the search criteria, then what value the user wants to search by.
        if search_by == "title":
            if search_query in song["title"].lower():
                filtered_songs.append(song)
        elif search_by == "artists":
            for artist in song["artists"]:
                if search_query in artist.lower():
                    filtered_songs.append(song)
                    break  # No need to check other artists
        elif search_by == "genres":
            for genre in song["genres"]:
                if search_query in genre.lower():
                    filtered_songs.append(song)
                    break  # No need to check other genres

    # Remove explicit songs if the user doesn't want them
    if not include_explicit:
        #Loop and add all clean songs
        songs_to_keep = []
        for song in filtered_songs:
            if not song.get("explicit", False):
                songs_to_keep.append(song)
        filtered_songs = songs_to_keep 

    # Sort based on the user's choice
    if sort_by == "popularity":
        #Sort in descending popularity
        filtered_songs.sort(key=sort_by_popularity, reverse=True)
    elif sort_by == "duration_mins":
        #Sort in ascending duration
        filtered_songs.sort(key=sort_by_duration)

    return jsonify(filtered_songs)

if __name__ == "__main__":
    app.run(debug=True)