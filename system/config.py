import configparser
import pathlib

config_parser = configparser.ConfigParser()

root_path = pathlib.Path(__file__).parent.parent.absolute()
config_path = root_path / "config" / "gameboa.config"

defaults = {
    "paths" : {
        'roms' : root_path / "roms",
        'saves' : root_path / "saves",
        'game configs': root_path / "config" / "game_configs",
        'patch files': root_path / "patches",
    },
    "video" : {},
    "sound": {},
    'input': {},
    'developer': {}
}


def load_config():
    config_parser.read_dict(defaults)
    config_parser.read(config_path)

def get_config(section, key):
    return config_parser[section][key]

def gat_as_data_type(section, key):
    value = get_config(section, key)
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