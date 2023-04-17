# English Words Suggester

## Set up
- Create the MYSQL database and their tables for the project
```sql
CREATE DATABASE `english-words-suggester`;

USE `english-words-suggester`;

CREATE TABLE english_words (
  id INT AUTO_INCREMENT PRIMARY KEY,
  word VARCHAR(255),
  count BIGINT UNSIGNED,
  skip BOOLEAN
);

CREATE TABLE settings (
  `name` VARCHAR(255) PRIMARY KEY,
  `val` INT
);
```
- Create the corresponding user for the database
```sql
CREATE USER 'english-words-suggester'@'localhost'; 
GRANT SELECT, INSERT, UPDATE, DELETE ON `english-words-suggester`.* TO 'english-words-suggester'@'localhost'; 
ALTER USER 'english-words-suggester'@'localhost' IDENTIFIED BY 'english-words-suggester';
```
