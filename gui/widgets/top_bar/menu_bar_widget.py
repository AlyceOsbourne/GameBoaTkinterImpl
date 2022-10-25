# main file bar for the window
from tkinter import *
from system.event_handler import EventHandler


class MenuBarWidget(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Rom", command=lambda: EventHandler.publish("Load Rom"))
        file_menu.add_command(label="Unload Rom", command=lambda: EventHandler.publish("Unload Rom"))
        file_menu.add_command(label="Exit", command=lambda: EventHandler.publish('Quit'))
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Settings", command=lambda: EventHandler.publish('OpenSettings'))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: EventHandler.publish('OpenAbout'))
        menubar.add_cascade(label="Help", menu=help_menu)


