**App info**  
The app, named "Sound Finder," uses the Deezer API to search for songs using keywords, allows users to save search results into custom playlists, and provides features like random song generation, playlist removal, and search history management.
The user is presented with a menu:
- search by keyword : this will then ask user to name their playlist which will be the text file name
- random song generator: app prints random song from search history
- delete existing playlist - user can name an existing playlist and the programme will delete it
- delete search history - clears data from search history file
- exit - this option stops the app

**Installation**  
The app uses Deezer API 
- You need to sign up to deezer to access it https://developers.deezer.com/api
- No key setup necessary
  
Request package is used to handle API requests. 
Requests is available on PyPI:
$ python -m pip install requests

os module is used to delete a file containing a playlist. It's a built-in module and doesn't need installation. 

random module is used to print a random song from search history for the user. It's a built-in module and doesn't need installation. 