
from tkinter import *
import tkinter.ttk as ttk
import pygame
import time
from tkinter.filedialog import askopenfilename, askopenfilenames
from mutagen.mp3 import MP3
root = Tk()
root.title("MUSIC PLAYER")
pygame.mixer.init()

def play_song_time():
    # here we use stopped variable , so that no more than one looping of song occurs,
    if stopped:
        return
    # Grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000
    # throw temp label to get data
    #slider_label.config(text=f'slider: {int(my_slider.get())} and song pos: {int(current_time)}')
    # covert to time  format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    # getting active song from song box
    song = song_box.get(ACTIVE)
    # getting song path and playing song
    song = f'E:\music_try\{song}.mp3'
    # loading song wuth mutagen
    song_mut = MP3(song)
    # get song length in seconds and coverting in time format
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    current_time += 1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'song duration: {converted_song_length}/{converted_song_length}  ')
    elif paused:
        # because of this condition duration time and bar does not move , on it moves when pause is false
        pass
    elif int(my_slider.get()) == int(current_time):
        # slider has  not moved
        # updating slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=0)
    else:
        # slider has been moved
        # updating slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=my_slider.get())

        # covert to time  format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # output the current_time and  song_length to the status bar
        status_bar.config(text=f'song duration: {converted_current_time}/{converted_song_length}  ')

        #move alongg by one second
        next_time = int(my_slider.get())+1
        my_slider.config(value=next_time)

    # output the current_time and  song_length to the status bar
    # status_bar.config(text=f'song duration: {converted_current_time}/{converted_song_length}  ')
    # updating slider position value to current song position
    # my_slider.config(value=int(current_time))  # current_time(seconds) --> 0 1 2 3 4 5 6 7 8 increasing
    # updating time
    status_bar.after(1000, play_song_time)

def add_song():
    song = askopenfilename(initialdir=r'E:\music_try', title="choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    song = song.replace(r'E:/music_try/', '')
    print(song)
    song = song.replace(r'.mp3', '')
    song_box.insert(END, song)

def add_many_song():
    song_list = askopenfilenames(initialdir=r'E:\music_try', title="choose a songs", filetypes=(("mp3 Files", "*.mp3"),))

    for song in song_list:
        song = song.replace(r'E:/music_try/', '')
        song = song.replace(r'.mp3', '')
        song_box.insert(END, song)
def delete_song():
    # stop function  to reset slider and status bar and stop song from playing
    stop()
    # To remove clicked song in song listbox
    song_box.delete(ANCHOR)
    # after removal to stop the music if it is playing
    pygame.mixer.music.stop()

def delete_all_song():
    # stop function  to reset slider and status bar and stop song from playing
    stop()
    # To remove all songs in song listbox
    song_box.delete(0, END)
    # after removal to stop the music if it is playing
    pygame.mixer.music.stop()

def play():
    global stopped
    # setting global stopped variable to false to play song
    stopped = False

    song = song_box.get(ACTIVE)
    song = f'E:\music_try\{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # call play song time function from play to get song length
    play_song_time()
    # updating slider to position
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=0)

global stopped
stopped = False
def stop():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # stopping song from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # when there nothing selected status bar should be empty
    status_bar.config(text='')

    # stop variable to true
    global stopped
    stopped = True

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def forward():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = song_box.curselection()
    # next one returns a tuple which contains a number which song is played ex. (0,) --> 1st song is played
    next_one = next_one[0] + 1
    # getting next song from song box
    song = song_box.get(next_one)
    # getting song path and playing song
    song = f'E:\music_try\{song}.mp3'
    # condition to not exceed after last song
    if song != r'E:\music_try\.mp3':
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    else:
        return
    # clear active bar in playlist listbox
    song_box.selection_clear(0, END)
    # activate new song bar
    song_box.activate(next_one)
    # set active bar to next song
    song_box.selection_set(next_one, last=None)
def backward():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = song_box.curselection()
    # next one returns a tuple which contains a number which song is played ex. (0,) --> 1st song is played
    next_one = next_one[0] - 1
    # getting before song from song box
    song = song_box.get(next_one)
    # getting song path and playing song
    song = f'E:\music_try\{song}.mp3'
    # condition to not exceed before first song
    if song != r'E:\music_try\.mp3':
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    else:
        return
    # clear active bar in playlist listbox
    song_box.selection_clear(0, END)
    # activate new song bar
    song_box.activate(next_one)
    # set active bar to next song
    song_box.selection_set(next_one, last=None)

def slide(x):
    song = song_box.get(ACTIVE)
    song = f'E:\music_try\{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #slider_label.config(text=f'{int(my_slider.get())}/{int(song_length)}')

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    # current_volume = pygame.mixer.music.get_volume()


my_label = Label(root, text="SONGS ", fg='white', bg='black')
my_label.pack()

master_frame = Frame(root,  bg="black")
master_frame.pack(pady=20)

song_box = Listbox(master_frame, fg='green', bg='black', width=60, selectbackground='yellow', selectforeground='red', font=('Helvatical bold',12))
song_box.grid(row=0, column=0)


# creating frame for arranging buttons
controls_frame = Frame(master_frame, bg="black")
controls_frame.grid(row=1, column=0, pady=20)

# create volume label frame
volume_frame = LabelFrame(master_frame, text="VOLUME", fg='white', bg="black")
volume_frame.grid(row=0, column=1, padx=20)

left_btn_img = PhotoImage(file=r"C:\Users\Dell\Pictures\Buttons\left50.png")
pause_btn_img = PhotoImage(file=r"C:\Users\Dell\Pictures\Buttons\pause50.png")
play_btn_img = PhotoImage(file=r"C:\Users\Dell\Pictures\Buttons\play50.png")
stop_btn_img = PhotoImage(file=r"C:\Users\Dell\Pictures\Buttons\stop50.png")
right_btn_img = PhotoImage(file=r"C:\Users\Dell\Pictures\Buttons\right50.png")

forward_btn = Button(controls_frame,  image=left_btn_img, borderwidth=0,command=forward)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause(paused))
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)
backward_btn = Button(controls_frame, image=right_btn_img, borderwidth=0,command=backward)

forward_btn.grid(column=0, row=1, padx=(10), pady=10, sticky=E + W)
pause_btn.grid(column=3, row=1, padx=(10), pady=10, sticky=E + W)
play_btn.grid(column=2, row=1, padx=(10), pady=10, sticky=E + W)
stop_btn.grid(column=1, row=1, padx=(10), pady=10, sticky=E + W)
backward_btn.grid(column=4, row=1, padx=(10), pady=10, sticky=E + W)

# creating menu
my_menu = Menu(root)
root.config(menu=my_menu)

# creating add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add songs', menu=add_song_menu)
add_song_menu.add_command(label='Add one song to box', command=add_song)
add_song_menu.add_command(label='Add songs to box', command=add_many_song)

# create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Remove songs', menu=remove_song_menu)
remove_song_menu.add_command(label='Delete a song from playlist', command=delete_song)
remove_song_menu.add_command(label='Delete  songs from playlist', command=delete_all_song)

# status bar creation
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# create Music Position slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

# create volume_slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# create temporay label
#slider_label = Label(root, text="0")
#slider_label.pack(pady=10)

root.configure(bg="black")
root.mainloop()
