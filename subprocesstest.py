import os
from fltk import Fl_Button, Fl_Window, Fl, Fl_Hold_Browser, Fl_Menu_Bar, Fl_File_Browser, Fl_File_Chooser, FL_SINGLE, fl_dir_chooser, Fl_Output, Fl_add_handler, FL_SHORTCUT, Fl_event_key, FL_YELLOW, Fl_Text_Display, Fl_Return_Button, Fl_Group
import subprocess as sp
import signal


class SongList(Fl_Hold_Browser):
    """
    holds a list of all the songs the user can play, and has functionality
    to add/remove songs
    """
    def __init__(self, window, *args):
        super().__init__(*args)
        self.window = window
        self.songs = set()
        self.pid = 0
        self.currently_playing = 0

    def add_song(self, music_dir, filename):
        if (music_dir, filename) in self.songs:
            return
        self.songs.add((music_dir, filename))
        self.add(filename, (music_dir, filename))

    def choose_music_dir(self):
        music_dir = fl_dir_chooser(".", "")
        print('user chose', music_dir)
        self.ordered_songs = []
        if music_dir is None:
            return
        for filename in os.listdir(music_dir):
            self.ordered_songs.append((music_dir, filename))
        self.ordered_songs.sort(key=lambda x: x[1])
        self.clear()
        for music_dir, filename in self.ordered_songs:
            self.add(filename, (music_dir, filename))


    def remove_current_song(self):
        bv = self.value()
        if bv == 0:
            return
        self.stop_playing()
        music_dir, filename = self.data(bv)
        self.songs.remove((music_dir, filename))
        self.remove(bv)

    def hotkeyhot(self):
        Fl_Text_Display(0,20,300,40, "t = top, b = bot, c = cur")

    def play_current_song(self):
        if self.pid != 0:
            return
        selected_line = self.value()
        if selected_line == 0:
            return
        self.currently_playing = selected_line
        print('selected line', selected_line)
        print('data', self.data(selected_line))
        music_dir, filename = self.data(selected_line)
        self.pid = sp.Popen(["mplayer", os.path.join(music_dir, filename)])
        self.window.yellowb.value(filename)
        # --intf dummy (interface dummy to disable vlc gui)

    def stop_playing(self):
        if self.pid != 0:  # already playing
            self.pid.send_signal(signal.SIGTERM)
            self.pid = 0
            self.currently_playing = 0

    def play_next(self):
        bv = self.value()
        self.stop_playing()
        bv += 1
        if bv > self.size():
            bv = 1
        self.value(bv)
        self.play_current_song()

    def play_last(self):
        bv = self.value()
        self.stop_playing()
        bv -= 1
        if bv < 1:
            bv = self.size()
        self.value(bv)
        self.play_current_song()

    def select_top_song(self):
        print('should select top song')
        bv = self.value()
        # self.stop_playing()
        bv = 1
        self.value(bv)

    def select_bottom_song(self):
        bv = self.value()
        # self.stop_playing()
        bv = self.size()
        self.value(bv)

    def select_current_song(self):
        if self.currently_playing == 0:
            return
        self.value(self.currently_playing)

    def clear_all_songs(self):
        self.songs = set()
        self.clear()

def playb_cb(wid):
    song_list.play_current_song()

def stopb_on_click(widget):
    song_list.stop_playing()


def close_win(wid):
    song_list.stop_playing()
    wid.hide()

def nextb_cb(wid):
    song_list.play_next()

def prevb_cb(wid):
    song_list.play_last()

class MyWindow(Fl_Window):
    def __init__(self, w, h):
        super().__init__(w, h)
        print('hullo from init')
        self.begin()
        self.group = Fl_Group(0, 0, w, h)
        self.group.begin()
        self.resizable(self.group)
        self.song_list = SongList(self, 0, 110, 800, 600)
        self.yellowb = Fl_Output(0, 40, 800, 70)
        self.yellowb.color(FL_YELLOW)

win = MyWindow(750, 800)
song_list = win.song_list

menu = Fl_Menu_Bar(0, 0, 800, 40)

def menu_add(menu_item, data):
    song_list.choose_music_dir()

def menu_delete(deleteb):
    song_list.remove_current_song()

def menu_hotkey(menu_item):
    return

def menu_top(menu_item, data):
    song_list.select_top_song()

def menu_bottom(menu_item, data):
    song_list.select_bottom_song()

def menu_current(menu_item, data):
    song_list.select_current_song()

def menu_clear(menu_item, data):
    song_list.clear_all_songs()


# def hotkeyup(P):
    # song_list.select_top_song()

# def hotkeydown(A):
    # song_list.select_bottom_song()

# def hotkeycurrent(G):
    # song_list.select_current_song()
#menu_hotkey.tooltip(' t for top, b for bottom, c for current')

ret = menu.add("menu_add", 0, menu_add, 0, 0)
# ret = menu.add("hotkeys/remove", ord('d'), menu_delete, 0, 0)
menu.add("hotkeys/bottom", ord('b'), menu_bottom, 0, 0)
menu.add("hotkeys/top", ord('t'), menu_top, 0, 0)
menu.add("hotkeys/current running", ord('c'), menu_current, 0, 0)
# menuhotkey = menu.add("myhotkeys", 0, menu_hotkey)
menu.add("clear/clear all", ord('A'), menu_clear, 0, 0)
print('menu.add', ret)
menu.redraw()
# yellowb = Fl_Hold_Browser(0,40,30,400)
playb = Fl_Return_Button(150, 710, 150, 90, "@>")
playb.shortcut(ord("p"))
playb.tooltip("press p")
stopb = Fl_Button(450, 710, 150, 90, "@||")
stopb.shortcut(ord("s"))
stopb.tooltip("press s")
# pauseb = Fl_Button(140, 40, 70, 40, "@||")
# resumeb = Fl_Button(210, 40, 70, 40, "@|>")
deleteb = Fl_Button(600, 710, 150, 90, "delete")
deleteb.shortcut(ord("d"))
deleteb.tooltip("press d")
nextb = Fl_Button(300, 710, 150, 90, "@>|")
nextb.shortcut(ord("n"))
nextb.tooltip("press n")
prevb = Fl_Button(0, 710, 150, 90, "@|<")
prevb.shortcut(ord("l"))
prevb.tooltip("press l")
#def general_event(event):
#    print('got an event:', event)
#    if event == FL_SHORTCUT:
#        key = Fl.event_key()
#        # key is a keyboard code, eg 'a' will be 97.  we can get the number for a letter using ord
#        if key == ord('t'):
#            song_list.select_top_song()
#        elif key == ord('b'):
#            song_list.select_bottom_song()
#        elif key == ord('c'):
#            song_list.select_current_song()

# Fl_add_handler(general_event)  # install a handler that catches any events that weren't already handled

deleteb.callback(menu_delete)
playb.callback(playb_cb)
stopb.callback(stopb_on_click)
win.callback(close_win)
nextb.callback(nextb_cb)
prevb.callback(prevb_cb)
# menuhotkey.callback(menu_hotkey)

win.end()
# win.size_range(800, 800, 900, 900)
win.show()
Fl.run()

# things we need:
# menu button that tells us the button to skip up and down and back to playing song 4
# text taht hovers over the buttons telling us quick keys 5
# forward and backward buttons 2
# yellow menu button that says what song playing  3
# button that removes stuff 1
# remove all Fl_Output (set string to " ") 6 - nvmd made function using menu+submenu
