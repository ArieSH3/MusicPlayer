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


	TO DO LIST:
	
	- *** Set up frames in tkinter as children of main root and dont pack, but grid them ***
		  so new frame can be added as grid(column=0, row=2, columnspan=2) in which
		  a song timetracker will be placed (It will be a bit of work and probably wont look
		  the same)

		  _______________________________
		  | ____________  ______________ |
		  ||		||		||
		  ||  controls	||     list	||
		  ||____________||______________||
		  | ____________________________ |
		  ||        time tracker        ||
		  ||____________________________||
		  |______________________________|
'''
import pygame
import os
import sys
import pprint
import time
import tkinter as tk

class MusicPlayer:

	def __init__(self, files_location:str) ->str: # Needs location of music folder
		self.s_list = []  # list of songs
		self.player_volume = 100 # player volume (Can be made to remember previously chosen volume)
		self.files_location = files_location
		self.__audio_paused = False
		self.__fadeout = 300 # Fadeout duration for song stop
		self.current_song = None
		self.song = 0

		pygame.mixer.init()

	
	# def options(self):
	# 	print('Player options:')
	# 	print(' song_list()')
	# 	print(' get_song()')
	# 	print(' play_song()')
	# 	print(' pause_song()')
	# 	print(' next_song()')
	# 	print(' previous_song()')
	# 	print(' show_volume()')
	# 	print(' change_volume()')
	# 	print(' shuffle()\n')

	
	def song_list(self, num=None): # Show a [list] of all available songs
		# Pretty print used for printing a list in a more readable manner
		
		# pp = pprint.PrettyPrinter(indent=4)
		# pp.pprint(os.listdir(self.files_location))
		# print('Length: ', len(os.listdir(self.files_location)))
		
		# for s in range(len(os.listdir(self.files_location))):
		# 	print(f'{s}:',os.listdir(self.files_location)[s].split('.')[0])
		# print()
		if num==None:
			return os.listdir(self.files_location)
		else:
			return os.listdir(self.files_location)[num]

	# def show_song_list(self):
	# 	for s in range(len(os.listdir(self.files_location))):
	# 		print(f'{s}:',os.listdir(self.files_location)[s].split('.')[0])
	# 	print()

	
	def get_song(self, song): # Pick and load the song in the player
		self.song = song
		if self.current_song == None:
			self.current_song = self.song
		#return self.song

	
	def play_song(self): # Play loaded song
		# Checks if current song is the same as the picked song and
		# if not then it means that user chose another song and is trying
		# to play it. This code then acts accordingly
		if self.song != self.current_song:# and self.current_song != None:
			self.current_song = self.song
			pygame.mixer.music.load('/'.join((self.files_location, self.song_list()[self.current_song])))
			pygame.mixer.music.play()

		if self.__audio_paused: # Checks if song is paused (Means it is already loaded and played) and unpauses it
			pygame.mixer.music.unpause()
			print('Unpaused')
			self.__audio_paused = False
		# Checks if audio paused and if audio is already playing then play_song wont rewind it but instead
		# it will do nothing thanks to (not pygame.mixer.music.get_busy()) check
		elif not self.__audio_paused and not pygame.mixer.music.get_busy(): # Checks if song is not paused(means it still isnt loaded and played)
			pygame.mixer.music.load('/'.join((self.files_location, self.song_list()[self.current_song])))
			pygame.mixer.music.play()
			print('Playing: ', self.song_list()[self.song].split('.')[0])

		self.current_song = self.song


	def pause_song(self): # Pause current song
		self.__audio_paused = True
		pygame.mixer.music.pause()
		print('Paused')

	def stop_song(self): # Stop current song
		pygame.mixer.music.stop()
		#pygame.mixer.music.fadeout(self.__fadeout) #Can bug out the player
		pygame.mixer.music.unload()
	
	def next_song(self): # Play next song in the list if available
		self.stop_song()
		# Plays next song in list
		try:
			self.get_song(self.song+1)
			self.play_song()
		# If error then it goes to the beginning of the list (Might be a crude way to do it but it works)
		except IndexError:
			self.get_song(0)
			self.play_song()

	def previous_song(self): # Play previous song in the list if available
		# Checks if song has been playing less than 10 seconds and if so it goes to previous song
		if pygame.mixer.music.get_pos()/1000 <= 10:
			# Plays previous song in list
			# If on first song (which is 0 in list) it will turn it to -1 which means
			# it goes back to the back of the list which works out perfectly
			self.stop_song()
			self.get_song(self.song-1)
			self.play_song()
		
		# If song has playes more than 10 seconds it will go back to the beggining of the same song
		# Same as rewind
		elif pygame.mixer.music.get_pos()/1000 > 10:
			self.stop_song()
			self.play_song()


	# def show_volume(self): # Show current volume (Can be used to mouseover icon to see volume)
	# 	print('Current volume: {}'.format(self.volume))
	
	# def change_volume(self, volume): # Change current volume
	# 	# Check that volume is withing acceptable range
	# 	if volume > 100:
	# 		self.volume = 100
	# 	elif volume < 0:
	# 		self.volume = 0
	# 	else:
	# 		self.volume = volume

	
	def volume(self, player_volume = 100): # Just show volume if no argument and show and change if there is argument
		# Volume returned as argument from scale method in tkinter
		# Divided by 100 cus set_volume takes values from (0.0 - 1.0)
		pygame.mixer.music.set_volume(int(player_volume)/100)


		# if player_volume != None:
		# 	try:
		# 		# Check that volume is withing acceptable range
		# 		if player_volume> 100:
		# 			self.player_volume = 100
		# 		elif player_volume < 0:
		# 			self.player_volume = 0
		# 		else:
		# 			self.player_volume = player_volume

		# 		print('Current volume: {}'.format(self.player_volume))

		# 	except TypeError:
		# 		print('Error: Value not a number')
		# else:
		# 	print('Current volume: {}'.format(self.player_volume))


	def song_position(self, song_time=None):
		pass


# Tkinter GUI
class MP_GUI:
	def __init__(self, root, files_location): # parent is the window/root(tk.Tk()) that is passed as argument to class
		self.music_player = MusicPlayer(files_location)
		
		self.root = root
		# < Create rest of GUI here >
		self.root.title('Music Player by ArieSH')
		self.root.geometry('700x400')
		self.root.config(bg='black')

		# FRAMEs
			# Left
		self.frame_left = tk.Frame(self.root)
		self.frame_left.pack(side='left', fill='both', expand=True)
		self.frame_left.config(bg='black')
			# Left Nested
		self.frame_left_inner = tk.Frame(self.frame_left)
		self.frame_left_inner.pack(pady=50, padx=50, fill='both')
		self.frame_left_inner.config(bg='black')
			# Bottom Nested
		self.frame_bottom_inner = tk.Frame(self.frame_left)
		self.frame_bottom_inner.pack(fill='both', padx=20)
		self.frame_bottom_inner.config(bg='black')
		# --------------------------------------------------------------
		
			# Right
		self.frame_right = tk.Frame(self.root)
		self.frame_right.pack(side='right', fill='both', expand=True)
		self.frame_right.config(bg='black')		
			# Right Nested
		self.frame_right_inner = tk.Frame(self.frame_right)
		self.frame_right_inner.pack(pady=50, padx=50, fill='both')
		self.frame_right_inner.config(bg='black')
		# --------------------------------------------------------------

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
		self.button_play = tk.Button(self.frame_left_inner, text='Play', image=self.img_play, font='none 10 bold', command=self.selected_song)
		self.button_play.config(activebackground='orange', bg='darkorange')
		self.button_play.pack(fill='both')
			# Pause
		self.button_pause = tk.Button(self.frame_left_inner, text='Pause', image=self.img_pause, font='none 10 bold', command=self.music_player.pause_song)
		self.button_pause.config(activebackground='orange', bg='darkorange')
		self.button_pause.pack(fill='both')
			# Stop
		self.button_stop = tk.Button(self.frame_left_inner, text='Stop', image=self.img_stop, font='none 10 bold', command=self.music_player.stop_song)
		self.button_stop.config(activebackground='orange', bg='darkorange')
		self.button_stop.pack(fill='both')
			# Previous
		self.button_previous_song = tk.Button(self.frame_left_inner, text='Previous', image=self.img_previous, font='none 10 bold', command=self.music_player.previous_song)
		self.button_previous_song.config(activebackground='orange', bg='darkorange')
		self.button_previous_song.pack(side='left', fill='both', expand=True)
			# Next
		self.button_next_song = tk.Button(self.frame_left_inner, text='Next', image=self.img_next, font='none 10 bold', command=self.music_player.next_song)
		self.button_next_song.config(activebackground='orange', bg='darkorange')
		self.button_next_song.pack(side='left', fill='both', expand=True)

		# LISTBOX
		self.listbox_music = tk.Listbox(self.frame_right_inner, selectmode='BROWSE')
		self.listbox_music.config(fg='darkorange', bg='black', highlightbackground='darkorange', highlightcolor='darkorange')

		tracker = 1
		for s in self.music_player.song_list():
			self.listbox_music.insert(tracker, s.split('.')[0])
			tracker += 1

		self.listbox_music.pack(fill='both')

		# SCALE
		self.scale_volume = tk.Scale(self.frame_bottom_inner, command=self.music_player.volume)
		self.scale_volume.config(highlightbackground='darkorange', bd=0, showvalue=0, orient='horizontal', length=100, troughcolor='black', activebackground='orange', bg='darkorange')
		self.scale_volume.set(100)
		self.scale_volume.pack(fill='both', expand=True)
	




	# Checks the selection in list and loads it to get_song method of
	# the MusicPlayer class
	def selected_song(self):
		for i in self.listbox_music.curselection():
			#print(i)
			# self.text_picked_song = tk.Text(self.frame_right_inner, height=5, width=20)
			# self.text_picked_song.insert(tk.END, self.music_player.song_list(i))
			self.music_player.get_song(i)
			self.music_player.play_song()


		

if __name__ == '__main__':

	files_location = 'Music'

	window = tk.Tk()
	MP_GUI(window, files_location)

	
	window.mainloop()
	











	# player = MusicPlayer(files_location)
	# player.options()
	# #player.volume(90)
	# player.show_song_list()
	# player.get_song(1) # Enter a number of a song you want to play
	# player.play_song()
	# time.sleep(5)
	# player.play_song()
	# time.sleep(5)
	# player.play_song()
	

	# input()
