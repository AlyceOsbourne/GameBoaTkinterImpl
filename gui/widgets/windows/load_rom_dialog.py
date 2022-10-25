from tkinter import filedialog
from system import EventHandler
import gzip
from system.config import config_parser

@EventHandler.subscriber('Load Rom')
def load_rom():
    file = filedialog.askopenfilename(
        initialdir=config_parser.get('paths', 'roms'),
        title="Select rom file",
        filetypes=(
            ("Gameboy", "*.gb"),
            ("Gameboy Color", "*.gbc"),
            ("Zip", "*.zip")
        ))

    if file:
        if file.endswith('.zip'):
            with gzip.open(file, 'rb') as f:
                rom = f.read()

        else:
            with open(file, 'rb') as f:
                rom = f.read()

        EventHandler.publish('Rom Loaded', rom)


