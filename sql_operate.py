import sqlite3
from web_retrieve import update_get
from hanziconv import HanziConv
import os.path
class SQL_Manager():
    def __init__(self,filename):
        self.file = filename

    def __enter__(self):
        # print("Open the database: {}".format(self.file))
        self.conn = sqlite3.connect(self.file)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print("Exit the database : {}".format(self.file))
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

def sql_build(sql):
    sql.execute('''CREATE TABLE IF NOT EXISTS novel
( 
  ID  INTEGER PRIMARY KEY,
  Name varchar(50) NOT NULL,
  url varchar(50) NOT NULL,
  unumber int NOT NULL
)
''')

def add_novel(novel_name, url, sql,index=0, dbfile='novel.db'):
    sql.execute('''INSERT INTO novel (Name, url, unumber)
                        VALUES (?, ?, ?)''', (novel_name, url, index))

def get_novel(sql):
    sql.execute('''SELECT Name, url, unumber FROM novel ''')
    return sql.fetchall()

def update_unumber(sql, name, unumber):
    sql.execute('''
UPDATE novel
SET unumber=?
WHERE Name=?
    ''',(unumber, name))

def find_update(dbfile='novel.db'):
    message = []
    update = 0
    with SQL_Manager(dbfile) as sql:
        novel = get_novel(sql)
        for (name, url, unumber) in novel:
            new_content = update_get(url, unumber)
            for (index, chapter, content) in new_content:
                content = HanziConv.toTraditional(content)
                r_str = "{} has new chapter, chapter {}: {}".format(name, chapter, content)
                message.append(r_str)
                update = index
            if update:
                # print("update unamber : {} to {}".format(update, name))
                update_unumber(sql, name, update)
    return message

# def sql_init(sql):
#         sql_build()
#         add_novel("逆天邪神", "https://www.piaotian.com/html/6/6760/index.html",index=6499820)
#         add_novel("修真聊天群", "https://www.piaotian.com/html/7/7580/index.html",index=6499820)



if __name__ == '__main__':
    with SQL_Manager("novel.db") as sql:
        sql_build(sql)
        # add_novel("逆天邪神", "https://www.piaotian.com/html/6/6760/index.html", sql, 6499820)
        # add_novel("大道朝天", "https://www.piaotian.com/html/9/9054/index.html", sql, 6508263)
        # add_novel("道君", "https://www.piaotian.com/html/8/8491/index.html", sql, 6508069)
        # add_novel("劍靈同居日記", "https://www.piaotian.com/html/8/8605/index.html", sql, 6506955)
        # add_novel("放開那個女巫", "https://www.piaotian.com/html/8/8025/index.html", sql, 6510206)
        # add_novel("修真聊天群", "https://www.piaotian.com/html/7/7580/index.html", sql, 6478632)
        for item in get_novel(sql):
            print(item)

    # with SQL_Manager('novel.db') as sql:
    #     update_unumber(sql, "修真聊天群", 6499820)
    #     update_unumber(sql, "逆天邪神", 6478632)
    # if os.path.isfile("./Data.db") == False:
    #     pass