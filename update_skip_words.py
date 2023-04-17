import os
import glob
import mysql.connector

# connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="english-words-suggester",
    password="english-words-suggester",
    database="english-words-suggester"
)

# get the last updated time from the database
cursor = connection.cursor()
cursor.execute("SELECT val FROM settings WHERE name = 'last_updated_time'")
last_updated_time = cursor.fetchone()[0]
cursor.close()

# get the folder path
FOLDER_PATH = "/home/hynduf/Documents/Obsidian/English Study/"

# get a list of all markdown files in the folder, sorted by modification time
files = sorted(glob.glob(os.path.join(FOLDER_PATH, "*.md")), key=os.path.getmtime)

# iterate over the files and update the database
for file_path in files:
    # get the modification time of the file
    mtime = os.path.getmtime(file_path)
    
    # if the modification time is less than the last updated time, break the loop
    if mtime < last_updated_time:
        break
    
    # get the file name and extension
    basename, ext = os.path.splitext(os.path.basename(file_path))
    
    # split the basename by spaces and convert to lowercase
    words = [word.lower() for word in basename.split()]
    
    # update the skip column for each word
    for word in words:
        cursor = connection.cursor()
        # print(word)
        cursor.execute("UPDATE english_words SET skip = TRUE WHERE word = %s", (word,))
        connection.commit()
        cursor.close()
        
        if cursor.rowcount > 0:
            print(f"Updated skip column for {word} in {file_path}")
    
# update the last_updated_time in the database
cursor = connection.cursor()
cursor.execute("UPDATE settings SET val = UNIX_TIMESTAMP() WHERE name = 'last_updated_time'")
connection.commit()
cursor.close()

# close the database connection
connection.close()
