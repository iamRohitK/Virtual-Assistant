import os    # The OS module in python provides functions for interacting with the operating system.
import subprocess as sp

paths = {
    'notepad': "C:\\Users\\itsro\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'music_dir': "C:\\MyFiles\\Entertainment\\Songs\\Hollywood"}

def open_notepad():
    os.startfile(paths['notepad'])
    # os.system('notepad')      
def close_notepad():
    os.system("taskkill /f /im notepad.exe")

def open_calculator():
    os.startfile(paths['calculator'])  
    # os.system('calc')      

def open_cmd():
    # os.system('start cmd')
    sp.call('start cmd', shell = True)

def open_camera():
    # os.system('start camera')
    # sp.run('start microsoft.windows.camera:', shell = True)
    sp.call('start microsoft.windows.camera:', shell = True)

def play_music():
    songs = os.listdir(paths['music_dir'])
    return songs
    # print(*songs, sep = '\n')    # It will print all the songs present in the music_dir


# print(os.getcwd())    # The current working directory is the folder in which the Python script is operating.