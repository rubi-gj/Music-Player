#WORKED BY: RUBEN GJATA
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pygame import mixer
import os
import random


root = Tk() #Initializes the main window using Tkinter.
root.title(" Music Player") #Title of the application
root.geometry("1000x600+1+10")#dimension of window+intial screen positions
root.configure(bg="#1e1e2f")# Configures the Background of the window
root.resizable(False, False)# Restricting to resize
mixer.init()   #Intializing the pygame mixer for audio playback

#Those variables are outside the function — they are  global
is_paused = False
is_shuffled = False
is_replay_mode = False
original_order = []  # To restore order after shuffle



#Node class represents each song in the playlist
class Node:
    def __init__(self, data):#Initialize a Node with data and pointers to the previous and next nodes.
        self.data = data #Store the data in the node
        self.prev = None #Pointer to the previous node (initialized to None)
        self.next = None #Pointer to the next node (initialized to None)


class CircularDoublyLinkedList:
    def __init__(self):    #Initialize the doubly linked list with head, tail, and current node pointers set to None
        self.head = None
        self.tail = None
        self.current_node = None

    def append(self, data):
        new_node = Node(data) # Create a new node with the provided data
        if self.head is None: # Check if the list is empty
            self.head = self.tail = new_node # If the list is empty, set the new node as both head and tail
            self.head.next = self.head.prev = self.head  # When the list has only one song (node), its next and previous should both point to itself.  This ensures the playlist remains circular and doubly linked, even with one item.
        else: # If the list is not empty, add the new node to the end of the list
            new_node.prev = self.tail   #Update new node's previous pointer
            new_node.next = self.head   #Update previous tail's next pointer to new node
            self.tail.next = new_node   #Update tail pointer to the new node
            self.head.prev = new_node   #Connect the head's previous to the tail
            self.tail = new_node        #Connect the tail's next to the head

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

    def rebuild_from_list(self, data_list):
        # Step 1: Clear the existing linked list completely
        self.head = None
        self.tail = None # Set head, tail, and current_node to None
        self.current_node = None
        # This deletes the old playlist structure so we can build a fresh one
        for data in data_list: #Loop through every item (song path) in the given list and add it to the playlist using the append() method
            self.append(data)  # Adding each song to the end of the new linked list

    def shuffle(self):
        items = self.to_list() #Convert the current linked list into a normal Python list ,it’s easier to shuffle a regular Python list than a linked list
        random.shuffle(items) #Use Python’s built-in shuffle to randomly reorder the items, this shuffles the song order in-place (modifies the list directly)
        self.rebuild_from_list(items) #Rebuild the entire linked list using the new shuffled order meaning throw away the old node structure and recreate it from scratch
        self.current_node = self.head #After rebuilding, reset the current_node to the new head (first song in shuffled list), this ensures the playlist knows where to start playing from after shuffling

    def play_next(self):
        if self.current_node and self.current_node.next:  #Move to the next node and return its data if it exists
            self.current_node = self.current_node.next #Updating current node with next node
            return self.current_node.data  #Returning the updated node
        elif self.current_node == self.tail: #Handle circular traversal to the head if currently at the tail, If current node is the first node then
            self.current_node = self.head   #Link the circular loop
            return self.current_node.data # Return the current node data
        return None # If nothing was there return None

    def play_previous(self):
        if self.current_node and self.current_node.prev: # Move to the previous node and return its data if it exists
            self.current_node = self.current_node.prev # Updating current node with prev node
            return self.current_node.data #Returning the updated node
        elif self.current_node == self.head: # Handle circular traversal to the head if currently at the tail, If current node is the first node then
            self.current_node = self.tail  # Link the circular loop
            return self.current_node.data  #Return the current node data
        return None # If nothing was there return None

    def get_song_at( self, index):  #Traverse the list to find the node at the given index and return its data
        current = self.head  # Start traversal from the head of the linked list
        count = 0  #Temp variable for counting
        while (current):  # Traverse the list until the current node is not None (end of the list)
            if count == index:  # If the value of count equals to index the
                return current.data  # return its data
            count += 1  # else increment count
            current = current.next  # update the current node with next node
        return None  # If nothing was there return None

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

playlist = CircularDoublyLinkedList() # Creating object for CircularDoublyLinkedList

#Functionalities
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

def pause_song():#Function to pause the song is playing
    global is_paused # Using keyword "Global" for a variable that lives outside this function without creating a new one inside
    mixer.music.pause()# Pause the currently playing audio using pygame mixer
    is_paused = True#   Now we are changing the variable is_paused, not creating a new one. Is going to pause a song

def resume_song():## Function to resume playback of a paused song
    global is_paused #Using keyword "Global" for a variable that lives outside this function without creating a new one inside
    mixer.music.unpause()#Resume the paused audio using pygame mixer
    is_paused = False#Now we are changing the variable is_paused, not creating a new one. Is going to play a song so making sure its not paused

def replay_song(): # This function restarts the current song from the beginning
    if playlist.current_node: #First, check if there is an active song
        current_song = playlist.current_node.data# Get the file path of the current song
        if os.path.exists(current_song):# Check if the song file still exists in the directory
            mixer.music.load(current_song) # Load the song file into the mixer for playback
            mixer.music.play() # Begin playing the loaded song from the start
            music.config(text=os.path.basename(current_song))#Update the label at the top of the window to show the song name, os.path.basename() takes the full file path like "C:/Music/.....mp3"
            index = playlist.to_list().index(current_song)# playlist.to_list() creates a regular Python list from our circular doubly linked list. It will look like this: ['C:/Music/song1.mp3', 'C:/Music/song2.mp3', 'C:/Music/song3.mp3'] Use index to find song at what number index it is
            List_of_songs.select_clear(0, END)#Clear any previous selection in the Listbox so  can highlight the current song
            List_of_songs.select_set(index)#Select highlight,  the current song in the GUI playlist
            List_of_songs.activate(index)#Focus it so it scrolls into view and becomes the active
        else:#If playlist.head is None, it means the playlist is empty or invalid than show an error message
            messagebox.showerror("Error", "File not found!")#Error Messages

def toggle_replay_mode():# This function toggles the repeat (replay) mode for songs
    global is_replay_mode # Declare we're using the global variable that tracks replay status
    is_replay_mode = not is_replay_mode # Flip the current replay state:  If it was OFF (False), it becomes ON (True)  or If it was ON (True), it becomes OFF (False)
    replay_button.config( #Update the replay button appearance to visually show the current state
        bg="#50fa7b" if is_replay_mode else "#44475a",
        text="🔁 Replay ON" if is_replay_mode else "🔁 Replay"
    )

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

def check_song_end():
    global is_paused #Using keyword "Global" for a variable that lives outside this function without creating a new one inside

    #Checking if the mixer is not busy
    if not mixer.music.get_busy() and not is_paused and playlist.current_node:
        if is_replay_mode:  #Cheking If replay mode is enabled
            replay_song()  #Replay the current song
        else:
            play_next_song() # Otherwise, move to the next song in the playlist


    root.after(1000, check_song_end)#Schedule this function to run again after 1 second (1000 milliseconds )


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

def show_song_time():
    if mixer.music.get_busy(): # Check If a song is currently playing
        pos = mixer.music.get_pos() // 1000    # Gets the current playback position in milliseconds and converts to seconds
        minutes = pos // 60 # Calculate how many minutes pass
        seconds = pos % 60 # Calculate the remaining seconds after the minutes
        song_time_label.config(text=f"Time: {minutes}:{str(seconds).zfill(2)}")# Update the label in the GUI to show the current time
                                                 #Both shows 2 digits
    root.after(1000, show_song_time)# Schedule this function to run again, this is a loop that the time keeps updating every second
                #Update every second
def clear_playlist():
    List_of_songs.delete(0, END) #Remove all songs from the Listbox in the GUI
    #Clear the actual linked list by resetting all its pointers
    playlist.head = None
    playlist.tail = None
    playlist.current_node = None

    music.config(text="Playlist Cleared") #Update the label at the top to let the user know the playlist has been cleared
    total_label.config(text="Total Songs: 0") #Update the bottom label to show there are now 0 songs

def delete_selected_song():
    selected = List_of_songs.curselection()#Get the index of the currently selected song in the GUI Listbox
                     # curselection using that returns a tuple to get the first  or the only selected item
    if selected: # Check if the user has actually selected something
        index = int(selected[0]) #Convert the selected index to an integer
        List_of_songs.delete(index) #Delete the selected song from the Listbox
        playlist.delete_at_index(index) #Remove the corresponding song from the circular linked list (in memory)
        
        show_total_songs()  #Update the song count label to reflect

# ----------------------- UI -----------------------
# -------------------- UI Elements --------------------

# Label to display the current song name
music = Label(root, text="", font=("Arial", 14, "bold"), fg="#00f7ff", bg="#1e1e2f")
music.place(x=400, y=20)  # Positioned near the top center

# Big title/header label at the top of the app
header = Label(root, text="🎧  Music Player", font=("Arial", 20, "bold"), fg="#ff2a6d", bg="#1e1e2f")
header.place(x=330, y=70)

# Frame to hold the song list (Listbox)
music_frame = Frame(root, bd=2, relief=RIDGE)
music_frame.place(x=30, y=130, width=400, height=300)

signature = Label(root, text="Worked by: Ruben Gjata", font=("Arial", 9, "bold"), fg="#aaaaaa", bg="#1e1e2f")
signature.place(x=800, y=570)

# Scrollbar for the song list
scroll = Scrollbar(music_frame)

# The Listbox that displays all loaded songs
List_of_songs = Listbox( music_frame,width=50,font=("Arial", 10),bg="#1e1e2f",fg="#8be9fd",cursor="hand2",bd=0,yscrollcommand=scroll.set)

# Connect scrollbar to Listbox scrolling
scroll.config(command=List_of_songs.yview)
scroll.pack(side=RIGHT, fill=Y)
List_of_songs.pack(side=LEFT, fill=BOTH)

# -------------------- Buttons --------------------

# Play the selected song
Button(root, text='🎵 Play', font=("Arial", 11), bg="#44475a", fg="white", command=play_song).place(x=460, y=180)

# Pause the current song
Button(root, text='⏸ Pause', font=("Arial", 11), bg="#44475a", fg="white", command=pause_song).place(x=560, y=180)

# Resume playback of paused song
Button(root, text='▶ Resume', font=("Arial", 11), bg="#44475a", fg="white", command=resume_song).place(x=660, y=180)

# Play previous song
Button(root, text='⏮ Prev', font=("Arial", 11), bg="#44475a", fg="white", command=play_previous_song).place(x=460, y=230)

# Play next song
Button(root, text='⏭ Next', font=("Arial", 11), bg="#44475a", fg="white", command=play_next_song).place(x=560, y=230)

# Toggle replay mode on/off
replay_button = Button(root, text='🔁 Replay', font=("Arial", 11), bg="#44475a", fg="white", command=toggle_replay_mode)
replay_button.place(x=660, y=230)

# Shuffle songs in playlist
Button(root, text='🔀 Shuffle', font=("Arial", 11), bg="#44475a", fg="white", command=shuffle_songs).place(x=760, y=230)

# Delete the selected song from playlist
Button(root, text='❌ Delete Song', font=("Arial", 11), bg="#44475a", fg="white", command=delete_selected_song).place(x=460, y=280)

# Clear entire playlist
Button(root, text='🧹 Clear', font=("Arial", 11), bg="#44475a", fg="white", command=clear_playlist).place(x=590, y=280)

# Open a folder and load all MP3s from it
Button(root, text='📂 Open Folder', font=("Arial", 11), bg="#44475a", fg="white", command=open_folder).place(x=700, y=280)

# -------------------- Extra UI --------------------

# Visual progress bar (not fully implemented but ready for extension)
progress = Progressbar(root, length=300, mode='determinate')
progress.place(x=500, y=330)

# Label that shows the total number of songs in playlist
total_label = Label(root, text="Total Songs: 0", font=("Arial", 10), fg="#f7f0e8", bg="#1e1e2f")
total_label.place(x=30, y=450)

# Label showing the current time position of the song
song_time_label = Label(root, text="Time: 0:00", font=("Arial", 10), fg="#f7f0e8", bg="#1e1e2f")
song_time_label.place(x=850, y=450)

# -------------------- Start Background Tasks --------------------

# Continuously update song timer every second
show_song_time()

# Automatically switch to next song when current ends
check_song_end()

# -------------------- Start Application --------------------

# Starts the Tkinter main event loop (keeps the app running)
root.mainloop()

#WORKED BY: RUBEN GJATA

