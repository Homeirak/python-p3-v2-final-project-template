# lib/models/Student.py
from models.__init__ import CURSOR, CONN
from models.Course import Course

class Student:
    all = {}

    def __init__(self, first, last, phone, email, gpa, course_id, id=None):
        self.id = id
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.gpa = round(float(gpa), 1)
        self.course_id = course_id

    def __repr__(self):
        return (
            f"<Student {self.id}: {self.first} {self.last}, "
            f"Phone: {self.phone}, Email: {self.email}, "
            f"GPA: {self.gpa}, Course ID: {self.course_id}>"
        )


    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            first TEXT,
            last TEXT,
            phone TEXT,
            email TEXT,
            gpa REAL,
            course_id INTEGER,
            FOREIGN KEY(course_id) REFERENCES courses(id))
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS students")
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO students (first, last, phone, email, gpa, course_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (
            self.first, self.last, self.phone, self.email, self.gpa, self.course_id
        ))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, first, last, phone, email, gpa, course_id):
        student = cls(first, last, phone, email, gpa, course_id)
        student.save()
        return student

    def update(self):
        sql = """
            UPDATE students
            SET first = ?, last = ?, phone = ?, email = ?, gpa = ?, course_id = ?
            WHERE id = ?
        """   
        CURSOR.execute(sql, (
            self.first, self.last, self.phone, self.email, self.gpa, self.course_id, self.id
        ))
        CONN.commit()
    
    def delete(self):
        CURSOR.execute("DELETE FROM students WHERE id = ?", (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
    
    @classmethod
    def instance_from_db(cls, row):
        student = cls.all.get(row[0])
        if student:
            student.first = row[1]
            student.last = row[2]
            student.phone = row[3]
            student.email = row[4]
            student.gpa = row[5]
            student.course_id = row[6]
        else:
            student = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            student.id = row[0]
            cls.all[student.id] = student
        return student
    
    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM students").fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_class_id(cls, course_id):
        rows = CURSOR.execute("SELECT * FROM students WHERE course_id = ?", (course_id,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_email(cls, email):
        row = CURSOR.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        return cls.instance_from_db(row) if row else None