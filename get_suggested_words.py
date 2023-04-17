import mysql.connector

def get_next_words(connection, WORD_ID_LOWER_THRESHOLD):
    cursor = connection.cursor()

    # execute query
    query = "SELECT id, word FROM english_words WHERE skip = False AND id >= %s ORDER BY id LIMIT 10"
    cursor.execute(query, (WORD_ID_LOWER_THRESHOLD,))
    rows = cursor.fetchall()

    cursor.close()

    return rows


def update_skip_words(connection, word_ids):
    cursor = connection.cursor()

    # update skip = True for the given word IDs
    where_in = ','.join(['%s'] * len(word_ids))
    query = "UPDATE english_words SET skip = True WHERE id IN (%s)" % (where_in)
    cursor.execute(query, word_ids)
    rows_affected = cursor.rowcount

    cursor.close()
    connection.commit()

    return rows_affected


# establish connection
connection = mysql.connector.connect(
    host="localhost",
    user="english-words-suggester",
    password="english-words-suggester",
    database="english-words-suggester"
)
print('Connected to the database.')
cursor = connection.cursor()

# get the current word ID from the settings table
query = "SELECT val FROM settings WHERE name = 'WORD_ID_LOWER_THRESHOLD'"
cursor.execute(query)
result = cursor.fetchone()
WORD_ID_LOWER_THRESHOLD = int(result[0])
cursor.close()
while True:
    # get the next set of words
    words = get_next_words(connection, WORD_ID_LOWER_THRESHOLD)
    if not words:
        print("No more words to display.")
        break

    # display the words
    print("Next 10 words:")
    for index, word in enumerate(words):
        print(f"{index + 1:2}. {word[1]}")

    # ask the user if they want to mark the words as skipped
    answer = input("Mark these words as skipped? ([y]/n): ")
    if answer.lower() == "y" or answer.lower() == "":
        # update the skip status and WORD_ID_LOWER_THRESHOLD
        word_ids = [word[0] for word in words]
        rows_affected = update_skip_words(connection, word_ids)
        print(f"{rows_affected} words updated.")

        # query and display the next set of words
        continue
    else:
        break

# close connection
connection.close()
