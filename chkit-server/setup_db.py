import sqlite3

try:
    conn = sqlite3.connect("chkit_DB.db")

    # Messages table Sql Query
    message_tbl_sql = """
        CREATE TABLE IF NOT EXISTS messages (
          id INTEGER PRIMARY KEY ,
          user_id varchar(255) NOT NULL,
          room_id int(10) NOT NULL,
          text text NOT NULL,
          casted int(1) NOT NULL,
          m_timestamp date,
          tmpID int(10) UNIQUE
        )
        """

    # Room table SQL Query
    rooms_tbl_sql = """
        CREATE TABLE IF NOT EXISTS rooms (
          id INTEGER PRIMARY KEY ,
          room_name varchar(255) NOT NULL
        )
        """
    conn.execute(message_tbl_sql)
    conn.execute(rooms_tbl_sql)
    conn.close
except sqlite3.Error as e:
    print("Database error: %s" % e)
