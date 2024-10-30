# Copyright (c) 2024 Colin James Faletto
# Written for the Newport Robotics Group

import json
import os
import random
import requests
import sys

# Gets a list of every JSON file in the root folder and any subfolders
# Filters specifically for message log files
def get_json_list():

    json_files = []
    extra_json_files = []

    # Gets files in every directory
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".json"):
                # Every message log file is called "20xx-xx-xx.json", and the number 2 isn't used anywhere else
                if ("2" in file):
                    json_files.append(f"{root}/{file}\n")
                else:
                    # This file is kinda useless but nice to have
                    extra_json_files.append(f"{root}/{file}\n")

    # If no message log files were found, then the script must be running in the wrong place
    if len(json_files) == 0:
        raise ValueError("No message log files found")
    

    with open("json_list.txt","w") as file_list:
        file_list.writelines(json_files)
    with open("extra_json_list.txt","w") as extra_file_list:
        extra_file_list.writelines(extra_json_files)

# Checks through every message log file from get_json_list(), looks for messages with a 'files' section,
# and gets the download URL connected to each file. Consolidates these URLs into
# a single file.
def get_file_list():

    json_files = []
    files_to_download = []

    # File from get_json_list
    with open("json_list.txt","r") as file_list:
        json_files = file_list.readlines()

    for filename in json_files:
        # UTF-8 encoding must be specified or stuff breaks
        with open(filename.rstrip("\n"),"r",encoding="utf-8") as raw_file:
            file = json.load(raw_file)
            for message in file:
                if "files" in message:
                    for subfile in message["files"]:
                        # Not sure what a tombstone is, might be a file that was manually deleted
                        # Either way, tombstones break stuff
                        if subfile["mode"] != "tombstone":
                            try:
                                # Google Drive/Onedrive links are randomly sprinkled in here, and those aren't getting deleted
                                if "files.slack.com" in subfile["url_private"]:
                                    # idk why it's called "url_private", seems pretty public to me
                                    files_to_download.append(subfile["url_private"] + "\n")
                            except:
                                print(f"ERROR in message " + message["text"] +  " in file " +  filename)
    with open("files_to_download.txt","w") as files_to_download_file:
        files_to_download_file.writelines(files_to_download)


# Takes the list of URLs from get_file_list() and downloads them individually
def crawler():


    file_list = []

    # File from get_file_list
    with open("files_to_download.txt","r") as file:
        file_list = file.readlines()

    if not os.path.exists(f"{os.getcwd()}/zDownload"):
        # Called this folder "zDownload" so it would be at the bottom of the folder list, next to this file
        os.makedirs(f"{os.getcwd()}/zDownload")

    for file in file_list:
        file = file.rstrip("\n")

        # Opens HTTP stream
        response = requests.get(file,stream=True)
        # Checks for errors
        response.raise_for_status()

        
        # Gets the tentative path for where the file will be downloaded
        filepath = f"{os.getcwd()}/zDownload/{file.split("/")[5].split("?")[0]}" # Removes useless URL data to get the file name

        # Checks for duplicate file name in destination (there were sooooo many files called image.png)
        duplicate_file = os.path.exists(filepath)
        while duplicate_file:        
            if os.path.exists(filepath):
                #Original line: filepath = "zDownload\\" + 1 + filepath.lstrip("zDownload\\")
                #This is why there are so many files with a string of ones as the filename
                #The script originally broke bc i hit the file path character limit lol

                # Adds a random number to the start of the file name
                filepath = f"{os.getcwd()}/zDownload/{random.randint(1,10000)}{file.split("/")[5].split("?")[0]}"
            else:
                duplicate_file = False
        #print(filepath)


        with open(filepath,"wb") as downloaded_file:

            # Downloads file in chunks because lord gpt said so
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    downloaded_file.write(chunk)
        print(f"Downloaded {filepath}")
        
        
def main():
    print("Welcome to the Slack Crawler")
    try:
        print("Getting list of message log files...")
        get_json_list()
    except:
        print("An error occured while finding JSON files. Please make sure this file is in the *root* directory of the slack export folder (next to canvases.json, channels.json, etc.)")
        sys.exit()
    print("Getting list of file URLs in messages..")
    get_file_list()
    print("Downloading files...")
    crawler()
    print("Done!")

if __name__ == "__main__":
    main()