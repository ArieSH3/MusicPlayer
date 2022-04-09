'''
	Creating a fully functional music player
		Using classes and methods for:
			-display functions
				song_list
				get_song
				play_song
				pause_song
				next_song
				previous_song
				show_volume
				change_volume
				shuffle

	Later try and add GUI interface to connect all 
	those classes to actual buttons 


	 ______________________________________________________________________________________
	TO DO LIST:
	
	- *** Set up frames in tkinter as children of main root and dont pack, but grid them ***
		  so new frame can be added as grid(column=0, row=2, columnspan=2) in which
		  a song timetracker will be placed (It will be a bit of work and probably wont look
		  the same)														

		  _______________________________
		  | ____________  ______________ |
		  ||			||				||
		  ||  controls	||	   list		||
		  ||____________||______________||
		  | ____________________________ |
		  ||        time tracker        ||
		  ||____________________________||
		  |______________________________|														(DONE)
	 ______________________________________________________________________________________


	- ***Make a functional Add To Playlist button that will prompt the user to choose
	  a list of songs they wish to be added to the current song list and can choose 
	  from those select songs which one they will play
	  	
	  	**Also enable user to go in multiple folders to pull songs from 						(DONE)
	 ______________________________________________________________________________________

	
	- ***Set the ability to change the initial folder the program looks in when adding to playlist
		so the user doesn't have to either keep folder with music inside folder with music player
		or so that he doesnt have to go back every time to a different folder from the one where
		music player is.
			Maybe use the text file to save the folder path the program will read and 
			open by default every time it starts												(DONE)
	 ______________________________________________________________________________________

	- ***Make a functional Remove From Playlist button that will give the user an option to
		select and remove songs that they no longer want in the list(box)

		### ISSUE is that when trying to remove/pop elements that came from different folders
			it for some reason shows IndexError: pop index out of range
			(FIXED by changing the if check value from 
			playlist_songs >= song   to   playlist_songs > song) and now it works perfectly		 (DONE)
	 ______________________________________________________________________________________

	- *Maybe try to give option to expand the window with (root.geometry(higher res)) if it can
		be done that way and within that epansion keep more functionality like changing the pitch,
		bass and other things within the music you listen to. (HIGHLY UNLIKELY)
	 ______________________________________________________________________________________

	- **Add the music timeline(possibly with Scale) where it will update as music goes on and can
		be used to put song on specific time
	 ______________________________________________________________________________________

	- **Add shuffle and loop buttons
	______________________________________________________________________________________

	- **Add buttons that skip the song 10 seconds forward and 10 seconds backward every time they
		are clicked
	______________________________________________________________________________________
	
	- **Add a label that will show what song is currently being played and duration of the song  (DONE)
	______________________________________________________________________________________

	-


'''
import pygame
import os
import sys
import pprint
import time
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3 # Can access file metadata

class MusicPlayer:

	def __init__(self, files_location:str) ->str: # Needs location of music folder
		self.s_list = []  # list of songs
		self.player_volume = 100 # player volume (Can be made to remember previously chosen volume)
		self.files_location = files_location
		self.__audio_paused = False
		self.__fadeout = 300 # Fadeout duration for song stop
		self.current_song = None
		self.song = 0
		self.song_stopped = False
		self.playlist_songs = []

		pygame.mixer.init()

	
	def song_list(self, num): # Show a [list] of all available songs
		# if num == None:
		# 	return []#os.listdir(self.files_location)
		# else:
		return num

	
	# NEEDS WORK CUS I DONT KNOW WHATS WRONG AND HOW TO DO IT (FIXED!!!)
	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	
	# ***Needs a fix when adding additional songs to the listbox. It jumbles it up
	# and adds duplicates which is not playable then. (FIXED!!!)
	def add_to_playlist(self):
		self.filepath = filedialog.askopenfilenames(title='Import shapefile', initialdir=self.files_location, filetypes=[('Music Files','.mp3')])
		# Extracts song from filepath(tuple with full destination*MIGHT BE USED TO ACCESS FOLDERED SONGS)
		# Fills playlist_songs with full paths to the song so pulling songs from multiple folders should
		# present no issue
		for s in range(len(self.filepath)):
			if self.filepath[s] not in self.playlist_songs:
				self.playlist_songs.append(self.filepath[s])


	# Enable removal of songs from current playlist
	def remove_from_playlist(self, song):
		# Checks if index wont be out of bound since removing one lowers number of elements in a list
		# so if index higher than number of elements it will just remove the final element
		if len(self.playlist_songs) > song:
			self.playlist_songs.pop(song)
		else:
			self.playlist_songs.pop()


	def get_song(self, song): # Pick and load the song in the player
		self.song = song
		print('Song number: ', self.song)
		# if self.current_song == None:
		# 	self.current_song = self.song

	
	def play_song(self): # Play loaded song
		# Checks if current song is the same as the picked song and
		# if not then it means that user chose another song and is trying
		# to play it.
		# *Bug was that the song couldn't be changed with play button until the 
		# actual song ended on its own.
		# This code runs when the first song since program started is played
		if self.song != self.current_song:# and self.current_song != None:
			print(1)
			self.current_song = self.song
			pygame.mixer.music.load(self.playlist_songs[self.song])
			pygame.mixer.music.play()

		# Checks if song is paused (Means it is already loaded and played) and unpauses it
		if self.__audio_paused: 
			print(2)
			# FIX!: Checks if song is stopped and if so then it wont try to
			# unpause but instead just load and play the song again
			# *Bug was that if you pause a song and then stop it and try to play,
			# it would first unpause and then play it on the second click
			if self.song_stopped:
				print(3)
				pygame.mixer.music.load(self.playlist_songs[self.song])
				pygame.mixer.music.play()
				self.song_stopped = False
			# Else if paused and not stopped then it just unpauses it
			else:
				print(4)
				pygame.mixer.music.unpause()
				print('Unpaused')
				self.__audio_paused = False
		# Checks if audio paused and if audio is already playing then play_song wont rewind it but instead
		# it will do nothing thanks to (not pygame.mixer.music.get_busy()) check
		elif not self.__audio_paused and not pygame.mixer.music.get_busy(): # Checks if song is not paused(means it still isnt loaded and played)
			print(5)
			pygame.mixer.music.load(self.playlist_songs[self.song])
			pygame.mixer.music.play()
			#print('Playing: ', self.playlist_songs[self.song].split('.')[0])
			self.song_stopped = False


	def pause_song(self): # Pause current song
		self.__audio_paused = True
		pygame.mixer.music.pause()
		print('Paused')

	def stop_song(self): # Stop current song
		pygame.mixer.music.stop()
		#pygame.mixer.music.fadeout(self.__fadeout) #Can bug out the player
		pygame.mixer.music.unload()
		self.song_stopped = True
	
	def next_song(self): # Play next song in the list if available
		#self.stop_song()
		# Plays next song in list
		try:
			self.get_song(self.song+1)
			self.play_song()
		# If error then it goes to the beginning of the list (Might be a crude way to do it but it works)
		except IndexError:
			print('Final song in list!')
			# self.get_song(0)
			# self.play_song()

	def previous_song(self): # Play previous song in the list if available
		try:	
			# Checks if song has been playing less than 10 seconds and if so it goes to previous song
			if pygame.mixer.music.get_pos()/1000 <= 10:
				# Plays previous song in list
				# If on first song (which is 0 in list) it will turn it to -1 which means
				# it goes back to the back of the list which works out perfectly
				#self.stop_song()
				self.get_song(self.song-1)
				self.play_song()
			
			# If song has playes more than 10 seconds it will go back to the beggining of the same song
			# Same as rewind
			elif pygame.mixer.music.get_pos()/1000 > 10:
				self.stop_song()
				self.play_song()
		except IndexError:
			print('First song in list!')

	
	def volume(self, player_volume = 100): # Just show volume if no argument and show and change if there is argument
		# Volume returned as argument from scale method in tkinter
		# Divided by 100 cus set_volume takes values from (0.0 - 1.0)
		pygame.mixer.music.set_volume(int(player_volume)/100)


	def song_position(self, song_time=None):
		print(pygame.mixer.music.get_pos())

	def song_length(self):
		song_metadata = MP3(self.playlist_songs[self.song])
		song_duration_seconds = song_metadata.info.length
		
		day = song_duration_seconds // (24 * 3600)
		song_duration_seconds = song_duration_seconds % (24 * 3600)
		hour = song_duration_seconds // 3600
		song_duration_seconds %= 3600
		minutes = song_duration_seconds // 60
		song_duration_seconds %= 60
		seconds = song_duration_seconds

		print('Time: h:', int(hour), 'm:', int(minutes), 's:', int(seconds))

		return [int(day), int(hour), int(minutes), int(seconds)]


# Tkinter GUI
class MP_GUI:
	def __init__(self, root, files_location): # parent is the window/root(tk.Tk()) that is passed as argument to class
		self.music_player = MusicPlayer(files_location)

		self.theme_color = '#BDE038'
		self.theme_color_accent = '#D9296A'
		self.theme_bg_color = '#242824'
		self.font = 'Helvetica 10 bold'

		self.mult_browse_select = False
		
		self.root = root
		# < Create rest of GUI here >
			# Allow or not resize for x, y
		self.root.resizable(False, False)
		self.root.title('Music Player by ArieSH')
		self.root.geometry('700x400')
		self.root.config(bg=self.theme_bg_color)

		# FRAMEs
			# Left
		self.frame_left = tk.Frame(self.root)
		self.frame_left.config(bg=self.theme_bg_color, width=200, height=200)
		self.frame_left.grid(column=0, row=0)
			# Right
				# Upper
		self.frame_right_upper = tk.Frame(self.root)
		self.frame_right_upper.config(bg=self.theme_bg_color, width=200, height=200)
		self.frame_right_upper.grid(column=1, row=0, padx=40)
				# Lower
		self.frame_right_lower = tk.Frame(self.root)
		self.frame_right_lower.config(bg=self.theme_bg_color, width=200, height=200)
		self.frame_right_lower.grid(column=1, row=1)
			# Bottom
		self.frame_bottom = tk.Frame(self.root)
		self.frame_bottom.config(width=700, height=160, bg=self.theme_bg_color)
		self.frame_bottom.grid(column=0, row=2, columnspan=2)

		# IMAGES
			# Play
		self.img_play = tk.PhotoImage(file='Images/play.png')
		self.img_play = self.img_play.subsample(2)
			# Pause
		self.img_pause = tk.PhotoImage(file='Images/pause.png')
		self.img_pause = self.img_pause.subsample(2)
			# Stop
		self.img_stop = tk.PhotoImage(file='Images/stop.png')
		self.img_stop = self.img_stop.subsample(2)
			# Previous
		self.img_previous = tk.PhotoImage(file='Images/previous.png')
		self.img_previous = self.img_previous.subsample(2)
			# Next
		self.img_next = tk.PhotoImage(file='Images/next.png')
		self.img_next = self.img_next.subsample(2)
			
		# BUTTONS
			# Play
		self.button_play = tk.Button(self.frame_left, text='Play', image=self.img_play, command=self.selected_song)
		self.button_play.config(activebackground=self.theme_color_accent, bg=self.theme_color, width=200)
		self.button_play.grid(column=0, row=0, columnspan=2, pady=(50,0), padx=(40,0))
			# Pause
		self.button_pause = tk.Button(self.frame_left, text='Pause', image=self.img_pause, command=self.music_player.pause_song)
		self.button_pause.config(activebackground=self.theme_color_accent, bg=self.theme_color, width=200)
		self.button_pause.grid(column=0, row=1, columnspan=2, padx=(40,0))
			# Stop
		self.button_stop = tk.Button(self.frame_left, text='Stop', image=self.img_stop, command=self.stop_song_label_update)
		self.button_stop.config(activebackground=self.theme_color_accent, bg=self.theme_color, width=200)
		self.button_stop.grid(column=0, row=2, columnspan=2, padx=(40,0))
			# Previous
		self.button_previous_song = tk.Button(self.frame_left, text='Previous', image=self.img_previous, command=self.music_player.previous_song)
		self.button_previous_song.config(activebackground=self.theme_color_accent, bg=self.theme_color, width=97)
		self.button_previous_song.grid(column=0, row=3, padx=(40,0))
			# Next
		self.button_next_song = tk.Button(self.frame_left, text='Next', image=self.img_next, command=self.music_player.next_song)
		self.button_next_song.config(activebackground=self.theme_color_accent, bg=self.theme_color, width=97)
		self.button_next_song.grid(column=1, row=3)
			
			# Add To Playlist
		self.button_add_to_playlist = tk.Button(self.frame_right_lower, text='Add To Playlist', font='Helvetica 10 bold', command=self.update_listbox)
		self.button_add_to_playlist.config(font=self.font, activebackground=self.theme_color_accent, bg=self.theme_color, width=20)
		self.button_add_to_playlist.grid(column=0, row=0)
			# Remove From Playlist
		self.button_remove_from_playlist =tk.Button(self.frame_right_lower, text='Remove', font='Helvetica 10 bold', command=self.remove_song)
		self.button_remove_from_playlist.config(font=self.font, activebackground=self.theme_color_accent, bg=self.theme_color, width=20)
		self.button_remove_from_playlist.grid(column=0, row=1)	
			# Multiple/Browse Select
		self.button_mult_browse = tk.Button(self.frame_right_lower, text='Select Type', command=self.listbox_browse_to_multiple)
		self.button_mult_browse.config(font=self.font, activebackground=self.theme_color_accent, bg=self.theme_color, width=10)
		self.button_mult_browse.grid(column=1, row=0)

		
		# LISTBOX
		self.listbox_music = tk.Listbox(self.frame_right_upper, selectmode=tk.BROWSE)
		self.listbox_music.config(font=self.font, fg=self.theme_color, bg=self.theme_bg_color, highlightbackground=self.theme_color, highlightcolor=self.theme_color, width=50)
		self.listbox_music.pack(pady=(70,0))

		
		# SCALE
		self.scale_volume = tk.Scale(self.frame_left, command=self.music_player.volume)
		self.scale_volume.config(highlightbackground=self.theme_color, bd=0, showvalue=0, orient='horizontal', length=100, troughcolor=self.theme_bg_color, activebackground=self.theme_color_accent, bg=self.theme_color)
		self.scale_volume.set(100)
		self.scale_volume.grid(column=1, row=4, pady=(40,0))


		# LABEL
			# Selection Type
		self.label_selection_type = tk.Label(self.frame_right_lower, text='Browse')
		self.label_selection_type.config(font=self.font, bd=0, bg=self.theme_bg_color, fg=self.theme_color)
		self.label_selection_type.grid(column=1, row=1)
			# Current Song Playing
		self.label_current_song_playing = tk.Label(self.frame_bottom, text='')
		self.label_current_song_playing.config(width=90, bg=self.theme_bg_color, fg=self.theme_color, font=self.font)
		self.label_current_song_playing.grid(column=0, row=0, pady=10)

	# Checks the selection in list and loads it to get_song method of
	# the MusicPlayer class
	def selected_song(self):
		for i in self.listbox_music.curselection():
			#print(i)
			# self.text_picked_song = tk.Text(self.frame_right_inner, height=5, width=20)
			# self.text_picked_song.insert(tk.END, self.music_player.song_list(i))
			self.music_player.get_song(i)
			self.music_player.play_song()
			self.label_current_song_playing_update()

	def update_listbox(self, remove=None):
		# Checks if button to add song has been clicked(remove remains None/False)
		# or if remove song button has been clicked (remove changed to True)
		if not remove:
			self.music_player.add_to_playlist()
		else:
			print('working...')

		# Checks if tracker is >0 then it means there are some songs in the listbox
		# already and it clears the whole listbox and adds a new music playlist
		# so that there are no duplicates in listbox and out of range errors when playing
		# if tracker > 0:
		# 	self.listbox_music.delete(0,tk.END)
		# Adds songs from the music list to the listbox to be displayed and interacted with
		tracker = 0
		self.listbox_music.delete(0, tk.END)
		for s in self.music_player.playlist_songs:
			self.listbox_music.insert(tracker, s.split('/')[-1].split('.')[0])
			tracker += 1
			# if s.split('/')[-1].split('.')[0] in self.listbox_music.get(0,tk.END):
			# 	# print('Listbox   ',self.listbox_music.get(0,tk.END))
			# 	# print('Playlist   ',self.music_player.playlist_songs)
			# 	tracker = len(self.listbox_music.get(0,tk.END))
			# else:
			# 	self.listbox_music.insert(tracker, s.split('/')[-1].split('.')[0])
			# # Can add colour to individual list items
			# #self.listbox_music.itemconfig("end", bg = "purple")
			# 	tracker += 1

		#print(self.listbox_music.get(0,tk.END))

	def remove_song(self):
		# Has trouble removing songs if they are last in t
		for i in self.listbox_music.curselection():
			print('Song number to pop: ', i)
			#print(self.music_player.playlist_songs)
			self.music_player.remove_from_playlist(i)
			#print(self.music_player.playlist_songs)

		self.update_listbox(remove=True)


	def listbox_browse_to_multiple(self):
		if not self.mult_browse_select:
			self.listbox_music.config(selectmode = tk.MULTIPLE)
			self.label_selection_type.config(text='Multiple')
			self.mult_browse_select = True
			print('MULTIPLE')
		elif self.mult_browse_select:
			self.listbox_music.config(selectmode=tk.BROWSE)
			self.label_selection_type.config(text='Browse')
			self.mult_browse_select = False
			print('BROWSE')

	# Updates labels text to the song name currently played and its duration in minutes and seconds
	def label_current_song_playing_update(self):
		length = self.music_player.song_length()
		hours = length[1]
		minutes = length[2]
		seconds = length[3]

		if hours > 0:
			self.label_current_song_playing.config(text=self.music_player.playlist_songs \
			[self.music_player.song].split('/')[-1].split('.')[0] + ' (' + \
			str(hours) + 'h:' + str(minutes) + 'm:' + str(seconds) + 's)')

		else:
			self.label_current_song_playing.config(text=self.music_player.playlist_songs \
			[self.music_player.song].split('/')[-1].split('.')[0] + ' (' + \
			str(minutes) + 'm:' + str(seconds) + 's)')

	# Stops song and returns label text of current playing song to empty string
	def stop_song_label_update(self):
		self.music_player.stop_song()
		self.label_current_song_playing.config(text='')


# Reads the .txt file that has full path of the music folder stored in it and returns the string
def get_music_location():
	with open('music_folder_location.txt', 'r') as f:
		location = f.read()
		f.close()
		return location
		
		



		

if __name__ == '__main__':

	# Gets the file location that is set in a text file (Can be changed by user to any location
	# they keep their music at)
	files_location = get_music_location()

	window = tk.Tk()
	gui=MP_GUI(window, files_location)


	window.mainloop()
	