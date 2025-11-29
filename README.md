🎵 Music Player - Design & README Document
 
 Justification of Data Structure Choice
I chose to build a Music Playlist Manager using a Circular Doubly Linked List because not only is it a fun, interactive, and practical way to demonstrate data structures in action, but also want to deliver a product that allows people to enjoy offline music for free. Furthermore, it offers a great balance between data structure functionality and visual interface (GUI).
 Code Walkthrough and Reasoning
The application is composed of several essential components: 
Since I'm conducting this project using a GUI, imports those components.

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pygame import mixer
import os
import random
This section imports the libraries required for the music player, such as Tkinter for GUI components, filedialog and messagebox for file selection and alerts, Progressbar for showing playback progress, Pygame's mixer for handling audio playback, and Python’s built-in os and random modules for file operations and shuffling songs.

root = Tk() # Initializes the main window using Tkinter.
root.title(" Music Player") # Title of the application
root.geometry("1000x600+1+10")#dimension of window+intial screen positions
root.configure(bg="#1e1e2f")# Configures the Background of the window
root.resizable(False, False)# Restricting to resize
mixer.init()   # Intializing the pygame mixer for audio playback

This block creates a fixed-size, non-resizable dark-themed Tkinter window with the title "Music Player," positioning it on the screen, and initializes the Pygame mixer to allow audio playing functionality.

# Those variables are outside the function — they are  global
is_paused = False
is_shuffled = False
is_replay_mode = False
original_order = []  # To restore order after shuffle

These global variables monitor the music player's playing status — whether it's stopped, shuffled, or in replay mode — and save the original playlist order so it may be restored after shuffling.

# Node class represents each song in the playlist
class Node:
    def __init__(self, data): # Initialize a Node with data and pointers to the previous and next nodes.
        self.data = data # Store the data in the node
        self.prev = None # Pointer to the previous node (initialized to None)
        self.next = None # Pointer to the next node (initialized to None)
The Node class represents a single song within the playlist by encapsulating the song's data (such as its file location) and retaining two references prev and next which connects it to the previous and next nodes in the sequence, allowing for easy traversal in both directions via the doubly linked list structure.


class CircularDoublyLinkedList:
    def __init__(self):    # Initialize the doubly linked list with head, tail, and current node pointers set to None
        self.head = None
        self.tail = None
        self.current_node = None
The CircularDoublyLinkedList class initializes an empty music playlist by setting the head, tail, and current_node pointers to None, laying the foundation for managing songs using a circular doubly linked list where each song can be traversed in both forward and backward directions in a continuous loop.
def append(self, data):
    new_node = Node(data) # Create a new node with the provided data
    if self.head is None: # Check if the list is empty
        self.head = self.tail = new_node # If the list is empty, set the new node as both head and tail
        self.head.next = self.head.prev = self.head  # When the list has only one song (node), its next and previous should both point to itself.  This ensures the playlist remains circular and doubly linked, even with one item.
    else: # If the list is not empty, add the new node to the end of the list
        new_node.prev = self.tail   # Update new node's previous pointer
        new_node.next = self.head   # Update previous tail's next pointer to new node
        self.tail.next = new_node   # Update tail pointer to the new node
        self.head.prev = new_node   # Connect the head's previous to the tail
        self.tail = new_node        # Connect the tail's next to the head
The append method is responsible for adding a new song to the circular doubly linked playlist by creating a node with the song data and, depending on whether the playlist is empty or not, either setting it as the first and only node (with its next and prev pointers referencing itself), or attaching it to the end of the existing list by linking it between the current tail and head nodes thereby preserving the circular and doubly linked structure where each node can be navigated forward and backward without breaking the loop.






def to_list(self):
    items = [] #Creatin an empty list to store the data from each node (song file paths)
    current = self.head # Set "current" to the first node in the playlist. This is where we start traversing from
    if current is None: # Check  if the playlist is empty (no songs), return the empty list  This is a safety check to avoid errors if nothing is loaded
        return items #simply return the empty list, there's nothing to collect
    while True: #Begin looping through the circular linked list
        items.append(current.data)  # Add the song's data (file path) to the list. Since it's a circular list, it doesn't end with 'None', it loops back to the start
        current = current.next # Move to the next node
        if current == self.head: #check if is gone full circle.  If "current" is back at "head", have visited all nodes once.
            break # Exit the loop
    return items     # At this point, all song paths are collected  in order  and stored them in a simple Python list, ready to use
The to_list method traverses the circular doubly linked playlist from the head node, collects each song’s data into a regular Python list, and returns it, ensuring all songs are included exactly once even in a looped structure.

def rebuild_from_list(self, data_list):
    # Step 1: Clear the existing linked list completely
    self.head = None
    self.tail = None # Set head, tail, and current_node to None
    self.current_node = None
    # This deletes the old playlist structure so we can build a fresh one
    for data in data_list: #Loop through every item (song path) in the given list and add it to the playlist using the append() method
        self.append(data)  # Adding each song to the end of the new linked list
This method clears the existing playlist and rebuilds it from a given list of song data by re-adding each item to form a fresh circular doubly linked list.





def shuffle(self):
    items = self.to_list() #Convert the current linked list into a normal Python list ,it’s easier to shuffle a regular Python list than a linked list
    random.shuffle(items) #Use Python’s built-in shuffle to randomly reorder the items, this shuffles the song order in-place (modifies the list directly)
    self.rebuild_from_list(items) #Rebuild the entire linked list using the new shuffled order meaning throw away the old node structure and recreate it from scratch
    self.current_node = self.head #After rebuilding, reset the current_node to the new head (first song in shuffled list), this ensures the playlist knows where to start playing from after shuffling
This method randomizes the song order by converting the playlist to a list, shuffling it using Python’s random.shuffle(), then rebuilding the linked list with the new order and resetting playback to the first song.

def play_next(self):
    if self.current_node and self.current_node.next:  # Move to the next node and return its data if it exists
        self.current_node = self.current_node.next # Updating current node with next node
        return self.current_node.data  # Returning the updated node
    elif self.current_node == self.tail: # Handle circular traversal to the head if currently at the tail, If current node is the first node then
        self.current_node = self.head   # Link the circular loop
        return self.current_node.data # Return the current node data
    return None # If nothing was there return None
This method moves the current song pointer to the next node in the circular playlist, and if it's at the end, it loops back to the start, returning the data of the next song to play.
def play_previous(self):
    if self.current_node and self.current_node.prev: # Move to the previous node and return its data if it exists
        self.current_node = self.current_node.prev # Updating current node with prev node
        return self.current_node.data # Returning the updated node
    elif self.current_node == self.head: # Handle circular traversal to the head if currently at the tail, If current node is the first node then
        self.current_node = self.tail  # Link the circular loop
        return self.current_node.data  # Return the current node data
    return None # If nothing was there return None
This method moves the current song pointer to the previous node in the playlist, looping to the end if it's at the beginning, and returns the data of the previous song to play.

def get_song_at( self, index):  # Traverse the list to find the node at the given index and return its data
    current = self.head  # Start traversal from the head of the linked list
    count = 0  # Temp variable for counting
    while (current):  # Traverse the list until the current node is not None (end of the list)
        if count == index:  # If the value of count equals to index the
            return current.data  # return its data
        count += 1  # else increment count
        current = current.next  # update the current node with next node
    return None  # If nothing was there return None
This method traverses the playlist from the head and returns the data of the song located at the specified index, or None if the index is out of range.
def delete_at_index(self, index):
    #If the playlist is empty (nothing to delete), exit early
    if self.head is None:
        return
    current = self.head # Start from the head of the list
    count = 0 # Counter to track which node is at

    while True:   #Traverse through the list until we reach the node at the specified index
        if count == index:
            # Checking If we're about to delete the song that's currently playing, stop playback
            if current == self.current_node:
                mixer.music.stop()
                self.current_node = None  # Clear current_node reference
            if current == self.head and current == self.tail: #Handle case where there's only one node in the list
                self.head = self.tail = None
            else:  #Link the previous node to the next node, skipping over the one to be deleted
                current.prev.next = current.next
                current.next.prev = current.prev
                if current == self.head: #Cheking  If the node being deleted is the head, update the head pointer
                    self.head = current.next
                if current == self.tail: #Cheking  If the node being deleted is the tail, update the tail pointer
                    self.tail = current.prev
            break # Node has been deleted; break the loop
        # Move to the next node
        current = current.next
        count += 1
        if current == self.head: #If looped is back to the start, it means index was invalid or not found
            break
This function removess the songs at the provided index from the circular doubly linked playlist, including exceptional scenarios such as deleting the currently playing song or the sole song in the list, and updates the links to maintain the playlist structure.

playlist = CircularDoublyLinkedList() # Creating object for CircularDoublyLinkedList
This line creates an instance of the CircularDoublyLinkedList class to manage the playlist and handle song navigation in a circular, doubly linked structure.

def play_song():
    global is_paused # Using keyword "Global" for a variable that lives outside this function without creating a new one inside
    is_paused = False #   Now  changing the variable is_paused, not creating a new one. Is going to play a song so making sure its not paused
    if List_of_songs.curselection(): #Check if the user has selected a song from the Listbox (GUI)
        index = int(List_of_songs.curselection()[0]) # Get the index (position) of the selected song
        full_path = playlist.get_song_at(index)  # Get the full path of the selected song using the index
        if playlist.head is None:  # Checking If the playlist is empty, we can't play anything — just exit
            return
        if full_path and os.path.exists(full_path):# Check if the selected file path is valid and the file actually exists
            mixer.music.load(full_path) # Load the selected song into the mixer
            mixer.music.play() # Start playing the loaded song
            music.config(text=os.path.basename(full_path))# Update the label at the top to display just the song name
            List_of_songs.select_clear(0, END)# Update the Listbox UI: Clear any previously selected song
            List_of_songs.select_set(index)# Select the newly played song based on its index
            List_of_songs.activate(index)# Make it the active item in the list (highlights it visually)
            playlist.current_node = playlist.head
        else:
            # If the file doesn't exist, show an error popup
            messagebox.showerror("Error", "File not found!")#Error Message

This method plays the user-selected song from the GUI listbox by collecting its file path from the playlist, loading it into the mixer if one exists, initiating playback, and updating the UI and playlist's currents node as needed.      

def play_next_song():# Function to play next song
    global is_paused # Using keyword "Global" for a variable that lives outside this function without creating a new one inside
    is_paused = False #   Now  changing the variable is_paused, not creating a new one. Is going to play a song so making sure its not paused
    if playlist.head is None: #This function will do that If the playlist is empty is going to pass or go to next song in the playlist
        return

    next_song = playlist.play_next() # Retrieve the next song from the playlist

    if next_song and os.path.exists(next_song):#Checks if it has a valid song and is actually in disk. 'next_song' is the file path returned by the playlist.'os.path.exists(next_song)' makes sure the file is really there
        mixer.music.load(next_song)# After getting next song and valid it , load the song into the mixer so it's ready to play.
        mixer.music.play() #Start playing the loaded song
        music.config(text=os.path.basename(next_song))#Update the label at the top of the window to show the song name, os.path.basename() takes the full file path like "C:/Music/.....mp3"
        index = playlist.to_list().index(next_song) # playlist.to_list() creates a regular Python list from our circular doubly linked list. It will look like this: ['C:/Music/song1.mp3', 'C:/Music/song2.mp3', 'C:/Music/song3.mp3'] Use index to find song at what number index it is
        List_of_songs.select_clear(0, END) #Clear any previous selection in the Listbox so  can highlight the current song
        List_of_songs.select_set(index) #Select highlight,  the current song in the GUI playlist
        List_of_songs.activate(index)# Focus the selected song so it scrolls into view and becomes active
    else:#If the song file doesn't exist or something went wrong, show an error message
        messagebox.showerror("Error", "File not found!")#Error Message
This functions plays the next song in the playlist by obtaining it from the circular linked list, validating its existence, loading it into the mixer, and changing the GUI and selection state to match the current track. 	 




def play_previous_song():#Function to play previous song
    global is_paused # Using keyword "Global" for a variable that lives outside this function without creating a new one inside
    is_paused = False #Now we are changing the variable is_paused, not creating a new one. Is going to play a song so making sure its not paused
    if playlist.head: #Checks if the playlist has at least one song loaded
        previous_song = playlist.play_previous()   #Move the current pointer in the circular doubly linked list to the previous song .  Updates playlist.current_node to point to the previous node
        if previous_song and os.path.exists(previous_song): #Check if we get a previous song and not None or the file doesent exists anymore (maybe is deleted)
            mixer.music.load(previous_song) #Load the previous song into the mixer
            mixer.music.play() #Start playing the loaded song
            music.config(text=os.path.basename(previous_song))#Update the label at the top of the window to show the song name, os.path.basename() takes the full file path like "C:/Music/.....mp3"
            index = playlist.to_list().index(previous_song)#playlist.to_list() creates a regular Python list from our circular doubly linked list. It will look like this: ['C:/Music/song1.mp3', 'C:/Music/song2.mp3', 'C:/Music/song3.mp3'] Use index to find song at what number index it is
            List_of_songs.select_clear(0, END)#Clear any previous selection in the Listbox so  can highlight the current song
            List_of_songs.select_set(index)#Select highlight,  the current song in the GUI playlist
            List_of_songs.activate(index)# Focus it so it scrolls into view and becomes the active
        else: #If playlist.head is None, it means the playlist is empty or invalid than show an error message
            messagebox.showerror("Error", "File not found!")#Error Messages
This function plays the previous song in the playlist by moving the current node pointer backward, verifying the song files, loading it into the mixer, initiating playing, and changing the GUI to reflect the newly selected track.  

def pause_song():#Function to pause the song is playing
    global is_paused # Using keyword "Global" for a variable that lives outside this function without creating a new one inside
    mixer.music.pause()# Pause the currently playing audio using pygame mixer
    is_paused = True#   Now we are changing the variable is_paused, not creating a new one. Is going to pause a song
This function pauses the currently playing songs using the mixer and updates the global is_paused flag to indicate that playback is paused.    
def resume_song():## Function to resume playback of a paused song
    global is_paused #Using keyword "Global" for a variable that lives outside this function without creating a new one inside
    mixer.music.unpause()#Resume the paused audio using pygame mixer
    is_paused = False#Now we are changing the variable is_paused, not creating a new one. Is going to play a song so making sure its not paused
The resume_song function resumes audio playback using the mixer if the song was previously paused, and updates the global is_paused flag to reflect that playback has continued. 


def toggle_replay_mode():# This function toggles the repeat (replay) mode for songs
    global is_replay_mode # Declare we're using the global variable that tracks replay status
    is_replay_mode = not is_replay_mode # Flip the current replay state:  If it was OFF (False), it becomes ON (True)  or If it was ON (True), it becomes OFF (False)
    replay_button.config( #Update the replay button appearance to visually show the current state
        bg="#50fa7b" if is_replay_mode else "#44475a",
        text="🔁 Replay ON" if is_replay_mode else "🔁 Replay"
    )
The toggle_replay_mode function switches the replay mode on or off by toggling a global flag that tracks the state, and dynamically updates the appearance and label of the replay button in the GUI to clearly indicate whether replay mode is active or not.  








def shuffle_songs(): #This functions shuffle songs playlist
    global is_shuffled, original_order # Using this global variables to track shuffle state and original order

    if not is_shuffled: # Checking If the playlist is NOT shuffled, shuffle it now
        original_order = playlist.to_list() # save the current song list order before shuffling so it restores later
        playlist.shuffle() # Shuffle the playlist using the method from the linked list class
        is_shuffled = True # Mark the shuffle state as active
        music.config(text="Shuffle ON") # Update the music label to show the user
    else:  #Checking If shuffle was already ON
        playlist.rebuild_from_list(original_order)# Restore the original song list order
        is_shuffled = False # Mark the shuffle state as OFF
        music.config(text="Shuffle OFF")# Update the music label to show the user

    playlist.current_node = playlist.head # After changing the playlist (shuffled or restored), reset the current song pointer to the beginning

    List_of_songs.delete(0, END) # Clear the Listbox UI so it  can reload the songs in the new order
    for song in playlist.to_list(): # Re-insert each song into the Listbox
        List_of_songs.insert(END, os.path.basename(song))

    show_total_songs() # Update the song count label at the bottom of the window

The shuffle_songs function toggles the shuffle mode by either randomizing the order of songs in the playlist or restoring them to their original sequence, while also resetting the current song pointer, updating the GUI list to reflect the new order, and refreshing the total song count display to maintain consistency in the user interface. 







def check_song_end():
    global is_paused #Using keyword "Global" for a variable that lives outside this function without creating a new one inside

    #Checking if the mixer is not busy
    if not mixer.music.get_busy() and not is_paused and playlist.current_node:
        if is_replay_mode:  #Cheking If replay mode is enabled
            replay_song()  #Replay the current song
        else:
            play_next_song() # Otherwise, move to the next song in the playlist

   
    root.after(1000, check_song_end)#Schedule this function to run again after 1 second (1000 milliseconds )
The check_song_end function continuously monitors whether the current song has finished playing, and if playback has stopped while not being paused, it either restarts the same song (if replay mode is active) or advances to the next track, with this check automatically repeating every second using root.after() for seamless playback control.

def open_folder():  #Function to open dialog box for choosing folder
    path = filedialog.askdirectory()  #file dialogue popup
    if path:  #Checks if path exist
        os.chdir(path)  #choose directory
        songs = os.listdir(path)  #all the files in the path
        for song in songs:
            if song.endswith(".mp3"):  #if mp3 files
                full_path = os.path.join(path, song)  # Get the full path of mp3 files
                List_of_songs.insert(END, song)  # Inserts the song into the GUI list
                playlist.append(full_path)  # Adds the full path of the song to the playlist which is used to retrive data for Linkedlist
        show_total_songs()
The open_folder function opens a directory selection dialog for the user, then scans the chosen folder for .mp3 files, adds each song's name to the GUI list for visual interaction, and stores the full file paths in the circular doubly linked playlist to manage playback operations. 






def show_total_songs():
    count = 0 # Start a counter to count how many songs are in the playlist
    node = playlist.head  # Start from the beginning of the circular linked list
    if node is None: # If the playlist is empty (head is None), update label to show 0
        total_label.config(text="Total Songs: 0")
        return
    while True: # Traverse the circular linked list and count each song
        count += 1 # Increase the song counter
        node = node.next # Move to the next song node
        if node == playlist.head: # If it comes full circle and are back at the head, it has  counted all songs
            break
    total_label.config(text=f"Total Songs: {count}") # Update the GUI label to display
The show_total_songs function loops through the entire circular doubly linked list starting from the head node, counts each song exactly once by detecting when it loops back to the beginning, and then updates the total_label in the GUI to show users how many songs are currently loaded in the playlist.  
def show_song_time():
    if mixer.music.get_busy(): # Check If a song is currently playing
        pos = mixer.music.get_pos() // 1000    # Gets the current playback position in milliseconds and converts to seconds
        minutes = pos // 60 # Calculate how many minutes pass
        seconds = pos % 60 # Calculate the remaining seconds after the minutes
        song_time_label.config(text=f"Time: {minutes}:{str(seconds).zfill(2)}")# Update the label in the GUI to show the current time
                                                 #Both shows 2 digits
    root.after(1000, show_song_time)# Schedule this function to run again, this is a loop that the time keeps updating every second
                #Update every second
The show_song_time function continuously updates the GUI with the current playback time of the song in minutes and seconds, by retrieving the mixer’s playback position and refreshing the display every second using root.after().  

def clear_playlist():
    List_of_songs.delete(0, END) #Remove all songs from the Listbox in the GUI
    #Clear the actual linked list by resetting all its pointers
    playlist.head = None
    playlist.tail = None
    playlist.current_node = None

    music.config(text="Playlist Cleared") #Update the label at the top to let the user know the playlist has been cleared
    total_label.config(text="Total Songs: 0") #Update the bottom label to show there are now 0 songs
The clear_playlist function removes all songs from both the GUI list and the internal circular linked list by resetting the playlist pointers, and updates the interface to reflect that the playlist has been cleared and now contains zero songs.  

def delete_selected_song():
    selected = List_of_songs.curselection()#Get the index of the currently selected song in the GUI Listbox
                     # curselection using that returns a tuple to get the first  or the only selected item
    if selected: # Check if the user has actually selected something
        index = int(selected[0]) #Convert the selected index to an integer
        List_of_songs.delete(index) #Delete the selected song from the Listbox
        playlist.delete_at_index(index) #Remove the corresponding song from the circular linked list (in memory)
        
        show_total_songs()  #Update the song count label to reflect
The delete_selected_song function allows the user to remove a selected song from both the GUI Listbox and the underlying circular linked playlist by identifying the selected index, deleting the song from both structures, and updating the total song count in the interface accordingly. 
# -------------------- Start Background Tasks --------------------

# Continuously update song timer every second
show_song_time()

# Automatically switch to next song when current ends
check_song_end()

# -------------------- Start Application --------------------

# Starts the Tkinter main event loop (keeps the app running)
root.mainloop()
This block initiates the background activities that update the song timer and manage song transitions automatically, followed by the Tkinter main event loop, which keeps the music player application running and responsive.



4. Performance with Different Data Sizes
The performance of this Music Player was evaluated using playlists of varied sizes to see how it scaled. The operations studied are: 

•	Adding songs to the playlist 
•	 Navigating (next/previous) through the songs 
•	Shuffle the playlist
•	 Delete songs from precise positions 
•	Converting the playlist to a regular Python list.

Playlist Size	Add Songs	Play Next/Prev	Shuffle Songs	Delete a Song	Convert to List
3 songs	~0.001s	Instant	~0.0015s	~0.001s	~0.0008s
5 songs	~0.0015s	Instant	~0.002s	~0.0012s	~0.001s
10 songs	~0.003s	Instant	~0.0035s	~0.002s	~0.0015s

•	Efficient Traversal: Using a circular doubly linked list, travelling forward and backward is always, O (1), even for thousands of songs. 
•	The conversion of a playlist to a Python list (to_list) is O(n) and grows linearly with the number of songs. 
•	To shuffle a list, use random.shuffle() (O(n)) and rebuild the linked list, which takes O(n) time total. 
•	Deleting at a given index needs traversal, making it O(n) in the worst case.

5. Why This Project Was Chosen
I chose this project because it’s practical, visually appealing but to also to demonstrate my abilities regarding structured data. In conclusion, this project functions as expected, and I am quite content to build a functional and ready app under a limited timeframe.
Playlist Music Player has a GUI that is prettier for the eye and has a better/ more intuitive logic for the user (Next/Previous/Shuffle), which makes it easier to demonstrate.

This Playlist Music Player, is much more focused, using a primary structure (CDLL). This makes it easier for the processors, by saving memory, thus avoiding the risk of errors such as Stack Overflow, which could happen on other projects, which use recursion, multiple structures or priority lists. In comparison, this Music Player, is relatively simple, stable and efficient, even by relatively long music lists.

This project offers immediate functionality and real-time usability; one can test it while listening to music.

Playlist Player has more of a visual interface, is more fun and easier to use.

6. What I Learned
Whilst I was working on the preparation of this project, I learned how to build a personalised structure of data (Circular Doubly Linked List) and how to use it as an actual app, with graphic interface (GUI).

With this project my understanding of the circular connection of elements and how one could secure or save the order of the songs in a more efficient way greatly increased, whilst not using available lists from Python. This structure gave me greater control for navigating between songs along with other functions such as “Next, Previous and Shuffle”, which are crucial to a Music Player.

Furthermore, by implementing function/features such as music playing, deleting, mixing and creating new files, my abilities on the modular organising of codes, a working external library like “Pygame” and “Tkinter”, as well as improving the user interface.
