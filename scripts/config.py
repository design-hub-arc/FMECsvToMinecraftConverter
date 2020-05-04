import configparser
import os

"""
This file is used to load user-dependant configuration
information, such as where certain files are located.

The first time this file is run,
it will save the default configuration
information to .\\config.ini.
All subsequent runs will read the
config file.
"""

#https://docs.python.org/3/library/configparser.html
CONFIG = configparser.ConfigParser()

def loadDefaultConfig():
    dirs = {
        "fme": "C:\\Program Files\\FME\\fme.exe",
        "workspace": ".\\",
        "output": ".\\convertedData",
        "mc": "{0}{1}\\AppData\\Roaming\\.minecraft\\saves".format(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"))
    }
    CONFIG["DIRS"] = dirs
def loadConfigFile(path):
    CONFIG.read(path)
def saveConfigFile(path):
    with open(path, "w") as file:
        CONFIG.write(file)



if os.path.isfile("config.ini"):
    try:
        loadConfigFile("config.ini")
    except Exception as e:
        print("Failed to load config.ini. Using default configuration")
        print(e)
        loadDefaultConfig()
else:
    loadDefaultConfig()
    saveConfigFile("config.ini")

FME_PATH = CONFIG["DIRS"]["fme"]
WORKSPACE_RELATIVE_PATH = CONFIG["DIRS"]["workspace"]
OUTPUT_DIRECTORY_RELATIVE_PATH = CONFIG["DIRS"]["output"]
MC_SAVE_DIR = CONFIG["DIRS"]["mc"]
