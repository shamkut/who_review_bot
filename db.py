import sqlite3
import os

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_FOLDER, "db")
db_location = os.path.join(RESOURCE_DIR, "review.sqlite.db")


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(db_location)
        self.setup()

    def setup(self):
        stmt = "create table if not exists reviewer (" \
               "chat_id integer, reviewer text, last_review_date DATETIME DEFAULT (datetime('now','localtime')))"
        self.conn.execute(stmt)
        self.conn.commit()

    def close(self):
        self.conn.close()

    ############## Reviewers ################

    def is_reviewer_exists(self, chat_id, reviewer):
        stmt = "select reviewer from reviewer where chat_id = (?) and reviewer = (?)"
        args = (chat_id, reviewer,)
        l = list(self.conn.execute(stmt, args))
        return len(l) > 0

    def add_reviewer(self, chat_id, reviewer):
        stmt = "insert into reviewer (chat_id, reviewer) values (?, ?)"
        args = (chat_id, reviewer,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_reviewer(self, chat_id, reviewer):
        stmt = "delete from reviewer WHERE chat_id = (?) and reviewer = (?)"
        args = (chat_id, reviewer,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_next_reviewer(self, chat_id, reporter):
        stmt = "select reviewer from reviewer where chat_id = (?) and reviewer <> (?) order by last_review_date limit 1"
        args = (chat_id, reporter,)
        x = self.conn.execute(stmt, args).fetchall()
        if x:
            return x[0][0]
        else:
            return None

    def who_next_reviewer(self, chat_id):
        stmt = "select reviewer from reviewer where chat_id = (?) order by last_review_date limit 1"
        args = (chat_id,)
        x = self.conn.execute(stmt, args).fetchall()
        if x:
            return x[0][0]
        else:
            return None

    def get_reviewers(self, chat_id, order_by=1):
        stmt = "select reviewer, last_review_date from reviewer where chat_id = (?) and reviewer is not null order by (?)"
        args = (chat_id, order_by,)
        return [(x[0], x[1]) for x in self.conn.execute(stmt, args)]

    def update_time(self, chat_id, reviewer):
        stmt = "update reviewer set last_review_date = datetime('now','localtime') where chat_id = (?) and reviewer = (?)"
        args = (chat_id, reviewer,)
        self.conn.execute(stmt, args)
        self.conn.commit()
