"""
Sound Finder
The app uses the Deezer API to search for songs using keywords, allows users to save search results into
custom playlists, and provides features like random song generation, playlist removal, and search history management.

The app uses Deezer API to retrieve song data
- I signed up to deezer to access it https://developers.deezer.com/api
- No key setup necessary

Request package is used to handle API requests. Full documentation can be found on PyPi
Package can be installed using the following command: $ python -m pip install requests

os module is used to delete playlist files, it's built in and doesn't need installing.

random module is used to print random song from a list, it's built in and doesn't need installing.
"""

import requests  # package used for handling API requests
import os  # module used to delete playlist files
import random  # Module used to access a random item from an array of all songs

# saving two variables in a global scope in all caps to indicate they shouldn't be changed
SEARCH_HISTORY_FILE = "search-history.txt"  # File name for saving search history (do not change)
PLAYLISTS_FOLDER = "playlists"  # Folder to store playlists (do not change)

is_app_running = True


def search_by_keyword():
    """Search for songs by a keyword using Deezer API and save them into a playlist."""
    search_string = input("Search keyword: ").lower()
    # constructing the full URL by combining the base URL and the search string
    deezer_api_url = f"https://api.deezer.com/search/?q={search_string}&index=0&limit=100&output=json"
    response = requests.get(deezer_api_url)  # connect to the API to perform the search
    if response.status_code == 200:  # Check if the API call was successful
        data = response.json()  # extract data from the JSON response
        if data.get("data"):  # check if the search returned any results
            save_search_results_to_playlist(search_string, response)
        else:
            print("No songs found.")  # inform the user if no songs found
    else:
        print("Failed to retrieve songs. Please try again")  # inform the user if API call unsuccessful


def save_search_results_to_playlist(search_string, search_results_data):
    """
        Save search results into a text file in a user-friendly format and append songs to the search history file.
        Arguments:
            search_string (str): The keyword used for the search.
            search_results_data (Response): The API response containing search results.
    """
    search_results_data = search_results_data.json()["data"]  # extract data from search results

    # validate input from the user
    while True:
        playlist_name = input("Enter playlist name: ").strip().lower()
        # Validate and get a non-empty playlist name from the user
        if not playlist_name:
            print("Playlist name cannot be empty. Please enter a name.")
        # validate that playlist doesn't already exists
        elif os.path.exists(f"{playlist_name}.txt"):
            print(f"Playlist {playlist_name} already exists. Enter another playlist name.")
        else:
            playlist_file = os.path.join(PLAYLISTS_FOLDER, f"{playlist_name}.txt")
            break  # Exit the loop once playlist file is created

    # Add artist names and songs to a text file in a user-friendly format and append songs to the search history file
    with open(playlist_file, "w") as playlist_file, open(SEARCH_HISTORY_FILE, "a") as search_history_file:
        for song_data in search_results_data:  # iterate over the search results data list to get artist and song names
            artist_name = song_data["artist"]["name"][:50]  # Use string slicing to limit the number of characters to 50
            song_name = song_data["title"][:50]  # Use string slicing to limit the number of characters to 50
            # To make search results more accurate, check if the search string is in the artist or song name
            if search_string.lower() in artist_name.lower() or search_string.lower() in song_name.lower():
                playlist_file.write(f"Artist name: {artist_name}\n")  # add artist name into playlist file
                playlist_file.write(f"Song name: {song_name}\n\n")  # add song name into playlist file
                search_history_file.write(f"{song_name} by {artist_name},")  # add songs into search history file
    print(f"Playlist {playlist_name} has been saved")  # confirm to the user that the playlist has been saved


def clear_history():
    """Clear the search history by overwriting the existing content of the search history file."""
    with open(SEARCH_HISTORY_FILE, "w"):
        pass
    print("Search history deleted.")  # confirm to the user search history was deleted


def show_random_song():
    """Display a random song from the search history file to the user."""
    with open(SEARCH_HISTORY_FILE, "r") as source_file:
        content = source_file.read()  # save content of search history file in a variable

    if len(content) > 0:  # Check if there's any song history
        search_history_songs = content.split(",")  # use split() to create a list of songs
        # use the random module to print a random song from the list
        print(f"Your song is {random.choice(search_history_songs)}")
    else:
        print("You have no search history.")  # inform the user if no search history


def remove_playlist():
    """Remove an existing playlist file."""
    # ask user for playlist to remove and save playlist filename to variable
    playlist_to_remove = input("What playlist do you want to delete? ").strip().lower()
    playlist_filename = os.path.join(PLAYLISTS_FOLDER, f"{playlist_to_remove}.txt")

    # Check if the filename exists, and if it does, delete the file using the os module
    if os.path.exists(playlist_filename):
        os.remove(playlist_filename)
        print(f"Playlist {playlist_to_remove} was deleted.")  # confirm to the user playlist was deleted
    else:
        print(f"Playlist {playlist_to_remove} doesn't exist.")  # if no playlist found, inform the user


def exit_app():
    """Exit the application"""
    global is_app_running  # call global variable is_app_running and change to false, it will be used by menu function
    is_app_running = False
    print(get_app_status())  # print app status to confirm the app has been exited


def get_app_status():
    """Return the current status of the application."""
    return "The application is running." if is_app_running else "The application is closed. See you next time!"


def menu():
    """Display a menu to the user and execute selected actions based on user input."""
    options = {  # Menu options are stored in a dictionary with function names as values
        "1": search_by_keyword,
        "2": show_random_song,
        "3": remove_playlist,
        "4": clear_history,
        "5": exit_app
    }

    while is_app_running:  # print the menu to the user while the app is running; choosing 5 stops the loop
        print("\nMenu:")
        print("1. Search by a keyword and save a playlist ")
        print("2. Get a random song from your search history")
        print("3. Delete existing playlist")
        print("4. Delete search history")
        print("5. Exit\n")

        choice = input("Enter your choice: ")  # Ask the user to choose a number for their option
        print("")  # adding an empty line after user's input

        if choice in options:  # validate user's choice
            options[choice]()  # call the corresponding function
        else:
            print("Invalid choice. Please select a valid option.\n")  # inform the user if choice invalid


menu()
