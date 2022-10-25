import configparser
import pathlib

config_parser = configparser.ConfigParser()

root_path = pathlib.Path(__file__).parent.parent.parent.absolute()

local_path = root_path / 'local'
local_path.mkdir(exist_ok=True)

config_folder_path = local_path / "config"
config_folder_path.mkdir(exist_ok=True)
config_path = config_folder_path / "gameboa.config"

defaults = {
    "paths" : {
        'roms' : local_path / "roms",
        'saves' : local_path / "saves",
        'game configs': config_folder_path / "game_configs",
        'patch files': local_path / "patches",
    },
    "video" : {},
    "sound": {},
    'input': {},
    'developer': {}
}


def load_config():
    config_parser.read_dict(defaults)
    config_parser.read(config_path)
    for path in config_parser['paths'].values():
        path = pathlib.Path(path)
        path.mkdir(exist_ok=True)
    config_parser.write(open(config_path, 'w'))

def get(section, key):
    return config_parser[section][key]

def get_d(section, key):
    value = get(section, key)
    if value.isdecimal():
        return float(value)
    elif value.isdigit():
        return int(value)
    elif value.lower in [
        'true',
        'false'
    ]:
        return value.lower() == 'true'
    else:
        return value

load_config()