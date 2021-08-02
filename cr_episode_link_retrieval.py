import os

import colored
import tkinter
import pyautogui

from colored import stylize
from tkinter import *
from selenium import webdriver


# This program is meant to to complement youtube-dl, populating a text file with series episode links. It is also specifically for use with Crunchyroll and because using series links leads to near 100% errors when trying to download. Using episode links sidesteps this problem and never (for me anyways) led to errors.

# Enables headless operation
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True

# current_series = [] # Not to be used until replacement for cvl is ready
current_episode = [] # Will contain episodes from your archive file
crunchyroll_series = 'crunchyroll_series_list.txt' # COPY/PASTE series page links into this file
crunchyroll_episodes = 'cr_episode_list.txt' # Your list of episodes previously parsed

# If cr_episode_list.txt isn't in current directory then this will make it
if not crunchyroll_episodes in os.listdir():
    open(crunchyroll_episodes, 'w')

# Opens cr_episode_list.txt for reading and appends all lines to current_episode list duplicate checking
episode_list = open(crunchyroll_episodes, 'r')
for episode in episode_list.readlines():
    current_episode.append(episode)

# Use this section of code to make sure that your file is read and appended to current_episode before you run the code to prevent duplicate entries.
# current_episode = 
# for e in current_episode:
#     print(e)
# quit()

# Opens crunchyroll_series_list.txt for reading and assigns it to cvl
cvl = open('crunchyroll_series_list.txt', 'r')

root = Tk()
root.title('Crunchyroll: New Episodes')

# Creates a window within root so we can attach the scrollbar.
frame = Frame(root)
frame.pack()

# We're showing links written we're using a listbox and placing is on the left of frame.
listbox = Listbox(frame, width=125, height=50)
listbox.pack(side=LEFT)

# Creating the scrollbar and placing is on the right of frame.
sb = Scrollbar(frame, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

# Setting up the scrollbar for use.
listbox.configure(yscrollcommand=sb.set)
sb.config(command=listbox.yview)

pyautogui.alert('Please be patient as the program writes the episode links. If you have a lot of series for it to look through then it could take awhile.\n\nFor example, I tested it with 500 series and it took ~15 minutes to complete. One of which was One Piece.', 'NOTICE FOR USER')

with webdriver.Firefox(options=fireFoxOptions) as driver:
    list_entry = 0
    for titles in cvl.readlines():
        driver.get(titles)

        # Gets all links inside .episode which are the episode links including all dubbed versions
        parse_episode_list = driver.find_elements_by_class_name('episode')        
        for parse_episode in parse_episode_list:

            # looks in each a tag for href attribute
            parse_episode_link = parse_episode.get_attribute('href')
            episode_link = parse_episode_link.split('https://www.crunchyroll.com/')
            episode_link = episode_link[1]
            
            # Prevents writing duplicate links by checking current_episode list for it
            if episode_link + '\n' in current_episode: 
                # Used only for showing duplicate entries, you won't need it on
                # print(stylize('[ARCHIVED] ' + episode_link, colored.fg(196)))
                continue

            # Note: entries will not appear in archive until the entire specified series has been written
            else:
                # Appends episode link to the cr_episode_list.txt.
                episode_list = open(crunchyroll_episodes, 'a')
                episode_list.write(episode_link + '\n') 
                
                # Used only for showing whats been written, you won't need it on
                print(stylize('[WRITING] ' + episode_link, colored.fg(112)))

                # Below: Formatting for new episodes displayed using tkinter for aesthetic purpose only, you can safely comment this out.
                # Removes the episode ID.
                episode_link = episode_link[:-7]
                
                 # Splits series title from episode.
                episode_link = episode_link.split('/')

                series_title = episode_link[0].replace('-', ' ').title()

                # Replace the hyphen after episode number with a semi-colon
                episode_title = episode_link[1].replace('-', ': ', 2).replace('-', ' ').title()

                #Finalizes the formatting for display in list_entry
                episode_link = series_title + ' - ' + episode_title
                # Above: Formatting for new episodes displayed using tkinter for aesthetic purpose only, you can safely comment this out.

                #Inserts episode link into listbox and is displayed once the program has finished going through the entirety of cvl
                listbox.insert(list_entry, episode_link)                
                
        # Incrementing begins next series to load
        list_entry += 1
        listbox.pack(padx=5, pady= 10)
    driver.quit
root.mainloop()
    