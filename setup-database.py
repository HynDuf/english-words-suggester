import mysql.connector
import csv

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="english-words-suggester",
    password="english-words-suggester",
    database="english-words-suggester"
)

# Create a cursor object
cursor = connection.cursor()

# Open the CSV file
with open("unigram_freq.csv", "r") as csvfile:
    # Read the CSV file
    csvreader = csv.reader(csvfile)

    # Skip the first row (header row)
    next(csvreader)

    # Iterate over each row in the CSV file
    for row in csvreader:
        # Insert the row into the MySQL database
        cursor.execute("INSERT INTO english_words (word, count, skip) VALUES (%s, %s, FALSE)", row)
    cursor.execute('INSERT INTO settings (name, val) VALUES ("ID_WORDS_TO_SKIP", 2000)')

# Commit the changes
connection.commit()

# Close the cursor and MySQL database connection
cursor.close()
connection.close()
