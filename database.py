import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('./reddit.db', timeout=10)
print("Successfully connected ")
conn.execute('CREATE TABLE if not exists users (user_name TEXT PRIMARY KEY NOT NULL,hashed_password TEXT NOT NULL, full_name TEXT NOT NULL, email_id TEXT NOT NULL,date_created DATE NOT NULL, is_active INTEGER NOT NULL)')
conn.execute('CREATE TABLE if not exists post (post_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT NOT NULL, title TEXT, content TEXT NOT NULL, is_active_article TEXT, date_created INTEGER, date_modified INTEGER, url TEXT, community TEXT, UpVote INT NOT NULL, DownVote INT NOT NULL, FOREIGN KEY (user_name) REFERENCES users(user_name))')

print("Successfully created reddit database")
conn.close()
