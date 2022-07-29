import sqlite3
from unittest import result
from uuid import uuid4


class VoteDB:
    def __init__(self):
        self.conn = sqlite3.connect('vote.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        create_topic_query = """
        CREATE TABLE IF NOT EXISTS Topics (
            id VARCHAR(64) primary key not null,
            name VARCHAR(50) not null
        );"""
        create_vote_query = """
        CREATE TABLE IF NOT EXISTS Votes (
            id INTEGER primary key AUTOINCREMENT not null, 
            topic VARCHAR(64),
            choice_name VARCHAR(50),
            choice_count INT,
            FOREIGN KEY (topic) REFERENCES Topics(id)
        );"""
        self.conn.execute(create_topic_query)
        self.conn.execute(create_vote_query)
        self.conn.commit()

    def add_topic(self, topic_name):
        topic_id = str(uuid4())
        self.conn.execute(
            'INSERT INTO Topics (id, name) VALUES (?, ?)',
            (topic_id, topic_name)
        )
        self.conn.commit()

    def get_topic_names(self):
        """
        [
            {
                "topic_id": str
                "topic_name": str
            }
        ]
        """
        query = 'SELECT * FROM Topics'
        result = self.conn.execute(query)
        ret = []
        for data in result:
            print(data)
            ret.append({
                'topic_id': data[0],
                'topic_name': data[1]
            })
        return ret

    def get_topic(self, topic_id):
        """
            [
                (vote_id, choice_name, choice_count)
            ],
            topic_name
        """
        topic_name_query = 'SELECT name FROM Topics WHERE Topics.id = ?'
        topic_name_reault = self.conn.execute(
            topic_name_query, (topic_id,)).fetchone()
        topic_name = topic_name_reault[0]
        query = """
        SELECT id, choice_name, choice_count FROM Votes v
        WHERE v.topic = ?
        """
        result = self.conn.execute(query, (topic_id,))
        ret = []
        for data in result:
            cid, cname, ccount = data
            ret.append((cid, cname, ccount))
        return ret, topic_name

    def add_choice(self, topic_id, choice_name):
        query = """
        INSERT INTO Votes (topic, choice_name, choice_count) VALUES (?, ?, ?)
        """
        self.conn.execute(query, (topic_id, choice_name, 0))
        self.conn.commit()

    def vote(self, choice_id, topic_id):
        query = """
        UPDATE Votes SET choice_count = choice_count + 1 WHERE topic = ? and id = ?
        """
        self.conn.execute(query, (topic_id, choice_id))
        self.conn.commit()
