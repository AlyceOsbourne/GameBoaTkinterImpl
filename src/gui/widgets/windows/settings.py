# a tkinter window that has tabs for each section in the config,
# and we create the widgets based on the value of the config

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from src.system.config import gat_value, get_d, set_value, sections, section_options, option_type
from src.system.event_handler import EventHandler
class SettingsWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Settings')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.grab_set()
        self.focus()

        self.tabs = ttk.Notebook(self)
        for section in sections():
            frame = Frame(self.tabs)
            self.tabs.add(frame, text=section)
            for key in section_options(section):
                if option_type(section, key) == bool:
                    var = BooleanVar(frame, value=get_d(section, key))
                    val = Checkbutton(frame, text=key, variable=var, command=lambda: set_value(section, key, var.get()))
                elif option_type(section, key) == str:
                    if section == "paths":
                        var = StringVar(frame, value=get_d(section, key))
                        Label(frame, text=key).pack(anchor=W)
                        Entry(frame, textvariable=var).pack(anchor=W)
                        val = Button(frame, text='Browse',
                                     command=lambda: set_value(section, key, filedialog.askdirectory()))
                    else:
                        var = StringVar(frame, value=get_d(section, key))
                        val = Entry(frame, textvariable=var)
                elif option_type(section, key) == int:
                    var = IntVar(frame, value=get_d(section, key))
                    Label(frame, text=key).pack(anchor=W)
                    val = Spinbox(frame, from_=0, to=100, textvariable=var)
                elif option_type(section, key) == float:
                    var = DoubleVar(frame, value=get_d(section, key))
                    Label(frame, text=key).pack(anchor=W)
                    val = Spinbox(frame, from_=0, to=100, increment=0.1, textvariable=var)
                else:
                    raise TypeError(f'Unknown type {option_type(section, key)}')
                setattr(self, f'{section}_{key}', val)
                val.pack(anchor=W)
        self.tabs.pack()

        Button(self, text='Close', command=self.destroy).pack()
        Button(self, text='Save', command=self.save).pack()

    def save(self):
        for section in sections():
            for key in section_options(section):
                set_value(section, key, getattr(self, f'{section}_{key}').get())
        self.destroy()


@EventHandler.subscriber("OpenSettings")
def open_settings(root):
    SettingsWindow(root)

