# Playlist
This is a music playlist made in Python, with a GUI made using pyFLTK.

This program allows you to add and remove songs from your files, as well as navigate through your curated playlist.

## Screenshot of Gameplay

## About Project:
I made this project to learn how to subprocess. I chose to make a music-player because I thought it would be good practice for writing other programs that produce sounds or just call upon external programs. This proved to be a useful endeavor for when I developed my later game of Simon Says.

## How it works:
The playlist program uses Python's subprocessor to launch an external media player which handles the audio.

When the user selects a song, the program creates a subprocess that will launch MPlayer which will handle playing the audio under that song title. The subprocess will terminate once the audio ends or the user selects a different song. Pausing will not terminate the subprocess.

The UI has several buttons (and hotkeys) that allow the user to:
- Load in a folder from their computer to the playlist menu
- Play, pause, and stop songs
- Go to the next or previous song
- Remove individual songs
- Clear the playlist
- Sort songs into alphabetical order for easier navigation

## Challenges
I found some difficulty in ensuring there were no bugs when adding more music to the program, so once new songs were added, the updated playlist would reorder itself to make room for the new files anything added would be sorted and reordered alphabetically.

To handle this, I organized filenames in an array container that would compare every title in a for loop before they would be updated to display in the GUI.

Building this project gave me a lot more experience working with subprocessors and navigating the shell better, since I would frequently need it for copying and moving and renaming things in various folders.

## Future Improvements:
- Include a search bar for quick song look-ups
- Prevent non-mp3 and mp4 files from being included when loading another folder into the playlist
- Adding a song-shuffle button for the user to get randomly-ordered music

## How to Run Program:
1. Start the Program
   
   python3 playlist.py

3. Using Playlist:
- Download a few mp3 files (some are provided in this repo)
- Click the add option and select a directory containing your audio
- Click on a song to select it and press the play button
- Use the controls or hotkeys displayed above to stop, skip, or go back to a song
- Use the delete button to remove a selected song
- Use the clear button to clear all music from the playlist
- Hotkeys are listed at the top of the interface menu and in the button tooltips section

## Resources Used:
- Python
- PyFLTK
- Python Subprocessor Module
- Python Signal
- os File Handling
- MPlayer
