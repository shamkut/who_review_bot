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
               "chat_id integer, reviewer text, last_review_date DATETIME DEFAULT (datetime('now','localtime'))," \
               "skip_till_date DATETIME" \
               ");"
        self.conn.execute(stmt)
        stmt = "select name from pragma_table_info('reviewer') where name = 'skip_till_date'"
        l = list(self.conn.execute(stmt))
        if len(l) == 0:
            stmt = "alter table reviewer add column skip_till_date DATETIME;"
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
        stmt = "select reviewer from reviewer " \
               "where chat_id = (?) and reviewer <> (?) and (skip_till_date < datetime('now','localtime') or skip_till_date is null) " \
               "order by last_review_date limit 1"
        args = (chat_id, reporter,)
        x = self.conn.execute(stmt, args).fetchall()
        if x:
            return x[0][0]
        else:
            return None

    def who_next_reviewer(self, chat_id):
        stmt = "select reviewer from reviewer " \
               "where chat_id = (?) and (skip_till_date < datetime('now','localtime') or skip_till_date is null) " \
               "order by last_review_date limit 1"
        args = (chat_id,)
        x = self.conn.execute(stmt, args).fetchall()
        if x:
            return x[0][0]
        else:
            return None

    def get_reviewers(self, chat_id):
        stmt = "select reviewer, last_review_date, datetime(case when skip_till_date > datetime('now','localtime') then skip_till_date end) " \
               "from reviewer where chat_id = (?) and reviewer is not null " \
               "order by " \
                   "case when skip_till_date < datetime('now','localtime') or skip_till_date is null " \
                   "then last_review_date " \
                   "else skip_till_date " \
                   "end"
        args = (chat_id, )
        return [(x[0], x[1], x[2]) for x in self.conn.execute(stmt, args)]

    def update_review_time(self, chat_id, reviewer):
        stmt = "update reviewer set last_review_date = datetime('now','localtime') where chat_id = (?) and reviewer = (?)"
        args = (chat_id, reviewer,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_skip_date(self, chat_id, reviewer, ndays):
        stmt = f"update reviewer set skip_till_date = date('now','+{ndays} day','localtime') where chat_id = (?) and reviewer = (?)"
        args = (chat_id, reviewer,)
        self.conn.execute(stmt, args)
        self.conn.commit()
