# lib/models/Course.py
from models.__init__ import CURSOR, CONN

class Course:
    all = {}

    def __init__(self, teacher, classname, term, id=None):
        self.id = id
        self.teacher = teacher
        self.classname = classname
        self.term = term

    def __repr__(self):
        return f"<Course {self.id}: {self.teacher}, {self.classname},{self.term} >"


    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            teacher TEXT,
            classname TEXT,
            term TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS classes;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
    
        sql = """
            INSERT INTO courses (teacher, classname, term)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.teacher, self.classname, self.term))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, teacher, classname, term):
        course = cls(teacher, classname, term)
        course.save()
        return course

    def update(self):
        sql = """
            UPDATE courses
            SET teacher = ?, classname = ?, term = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.teacher, self.classname, self.term, self.id))
        CONN.commit()

    def delete(self):
        

        sql = """
            DELETE FROM courses
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def instance_from_db(cls, row):

        # Check the dictionary for an existing instance using the row's primary key
        course = cls.all.get(row[0])
        if course:
            # ensure attributes match row values in case local instance was modified
            course.teacher = row[1]
            course.classname = row[2]
            course.term = row[3]

        else:
            # not in dictionary, create new instance and add to dictionary
            course = cls(row[1], row[2], row[3])
            course.id = row[0]
            cls.all[course.id] = course
        return course

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM courses
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM courses
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, classname):
        sql = """
            SELECT *
            FROM courses
            WHERE classname is ?
        """

        row = CURSOR.execute(sql, (classname,)).fetchone()
        return cls.instance_from_db(row) if row else None

    