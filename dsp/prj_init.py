#!/usr/bin/python3.8
import os, platform

system = platform.system()
print("Creating virtual environment for " + system)
dir_path = os.path.dirname(os.path.realpath(__file__))


if system == "Linux":

    venv_dir = dir_path + "/linux_venv"

    os.system('python3.8 -m venv ' + venv_dir)
    print("virtual env created in: " + venv_dir)

    os.system('linux_venv/bin/python3.8 -m pip install -r ' + dir_path + '/requirements.txt')

elif system == "Windows":
    
    venv_dir = dir_path + "\windows_venv"
    print("virtual env created in: " + venv_dir)

    os.system('python -m venv ' + venv_dir)
    os.system('.\windows_venv\Scripts\python -m pip install -r' + dir_path + '/requirements.txt')

