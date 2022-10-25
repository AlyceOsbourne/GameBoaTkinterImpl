# a tkinter window that has tabs for each section in the config,
# and we create the widgets based on the value of the config

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from src.system.config import gat_value, get_d, set_value, sections, section_options, option_type, save_config
from src.system.event_handler import EventHandler
class SettingsWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Settings')
        self.geometry('500x500')
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.grab_set()
        self.focus()
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=BOTH, expand=True)
        self.make_sections()
        self.tabs.pack()
        Button(self, text='Save', command=self.save).pack(side=LEFT, fill=X, expand=True)
        Button(self, text='Close', command=self.destroy).pack(side=RIGHT, fill=X, expand=True)

    def make_sections(self):
        for section in sections():
            frame = Frame(self.tabs)
            frame.pack(fill=BOTH, expand=True)
            self.tabs.add(frame, text=section, padding=10)
            self.make_section_tab(frame, section)

    def make_section_tab(self, frame, section):
        for i, key in enumerate(section_options(section)):
            section_label = Label(frame, text=key)
            section_label.grid(row=i, column=0, sticky=W)
            opt_type = option_type(section, key)
            if opt_type == str:
                value = StringVar()
                value.set(gat_value(section, key))
                value.trace('w', lambda *args: set_value(section, key, value.get()))
                entry = Entry(frame, textvariable=value)
                entry.grid(row=i, column=1, sticky=W)
                if section in [
                    'paths'
                ]:
                    Button(frame, text='Browse', command=lambda: self.browse(section, key, entry)).grid(row=i, column=2, sticky=W)
            elif opt_type == int:
                value = IntVar()
                value.set(gat_value(section, key))
                value.trace('w', lambda *args: set_value(section, key, value.get()))
                entry = Entry(frame, textvariable=value)
                entry.grid(row=i, column=1, sticky=W)
            elif opt_type == float:
                value = DoubleVar()
                value.set(gat_value(section, key))
                value.trace('w', lambda *args: set_value(section, key, value.get()))
                entry = Entry(frame, textvariable=value)
                entry.grid(row=i, column=1, sticky=W)
            elif opt_type == bool:
                value = BooleanVar()
                value.set(gat_value(section, key))
                value.trace('w', lambda *args: set_value(section, key, value.get()))
                entry = Checkbutton(frame, variable=value)
                entry.grid(row=i, column=1, sticky=W)
            else:
                raise ValueError(f'Unknown option type {opt_type}')
            setattr(self, f'{section}_{key}', value)
            # add spacer
            Label(frame, text=' ').grid(row=i, column=1, sticky=W)



    def save(self):
        for section in sections():
            for key in section_options(section):
                set_value(section, key, getattr(self, f'{section}_{key}').get())
        save_config()
        self.destroy()

    def browse(self, section, key, entry):
        path = filedialog.askdirectory()
        if path:
            entry.delete(0, END)
            entry.insert(0, path)
            set_value(section, key, path)



@EventHandler.subscriber("OpenSettings")
def open_settings(root):
    SettingsWindow(root)

