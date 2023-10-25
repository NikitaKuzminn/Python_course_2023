""""
Homework 5_2:
============
Preamble
========
We have a database file (example.sqlite) in sqlite3 format with some tables and data.
All tables have 'author' column and maybe some additional ones.
Data retrieval and modifications are done with sqlite3 module by issuing SQL statements.
For example, to get all data from TABLE1::
    import sqlite3
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from TABLE1')
    data = cursor.fetchall()   # will be a list with data.
instead of getting all data at once, you can use .fetchone() calls and named expressions::
    while row:=cursor.fetchone():
        print(row)
To get a row with specific author equal to some value::
    import sqlite3
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from books where author=:author', {author:'Bradbury'})
    data = cursor.fetchall()  # will get all records with this name. You can also use .fetchone() to get one record.
in order to get record with author (sorted alphabetically) use SQL expression `SELECT * from books order by author asc limit 1`
in order to get record after specified (sorted alphabetically) use SQL expression `SELECT * from books where author > :author order by author limit`.
To get amount of records in table TABLE1, use `select count(*) from TABLE1` query.
Please refer to this documents for more information about how to retrieve data from sqlite database:
DBAPI: https://www.python.org/dev/peps/pep-0249/
sqlite3 module: https://docs.python.org/3/library/sqlite3.html
Task
====
Write a wrapper class TableData for database table, that when initialized with database name
and table acts as collection object (implements Collection protocol).
Assume all data has unique values in 'author' column.
So, if books = TableData(database_name='example.sqlite', table_name='books')
then
 -  `len(books)` will give current amount of rows in books table in database
 -  `books['Bradbury']` should return single data row for book with author Bradbury
 -  `'Yeltsin' in books` should return if book with same author exists in table
 -  object implements iteration protocol. i.e. you could use it in for loops::
       for book in books:
           print(book['author'])
 - all above mentioned calls should reflect most recent data.
 If data in table changed after you created collection instance, your calls should return updated data.
Avoid reading entire table into memory. When iterating through records, start reading the first record,
then go to the next one, until records are exhausted.
When writing tests, it's not always neccessary to mock database calls completely.
Use supplied example.sqlite file as database fixture file.
"""

import sqlite3


class TableData:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.database_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def __getitem__(self, author):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE author=?", (author,))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        else:
            raise KeyError(f"Author '{author}' not found in the table.")

    def __len__(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return cursor.fetchone()[0]

    def __contains__(self, author):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE author=?", (author,))
        count = cursor.fetchone()[0]
        return count > 0

    def __iter__(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        columns = [description[0] for description in cursor.description]
        for row in cursor:
            yield dict(zip(columns, row))


# Example:
if __name__ == '__main__':
    with TableData(database_name='example.sqlite', table_name='books') as books:
        print(len(books))
        for author in books:
            print(author['author'])
        print('Bradbury' in books)
        print(books['Bradbury'])
