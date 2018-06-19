import psycopg2
from web_retrieve import update_get
from hanziconv import HanziConv
import os.path

class SQL_Manager():
    def __enter__(self):
        # print("Open the database: {}".format(self.file))
        self.DATABASE_URL = "postgres://dcykkfqagjlmin:5c5dddeaed204f653b6d2a0eb2d30bd5ff2b59cbdc8bab3f6dbed10e7fe" \
                                        "c8920@ec2-23-23-130-158.compute-1.amazonaws.com:5432/d1vjeo80jvh9e"
        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


def sql_build(sql):
    sql.execute("CREATE TABLE IF NOT EXISTS novel (id seiral PRIMARY KEY, name varchar, url varchar, unumber integer);")

def add_novel(novel_name, url, sql, index=0):
    sql.execute("INSERT INTO novel (Name, url, unumber) VALUES (%s, %s, %s);", (novel_name, url, index))

def get_novel(sql):
    sql.execute("SELECT name, url, unumber FROM novel;")
    return sql.fetchall()

def update_unumber(sql, name, unumber):
    sql.execute("UPDATE novel SET unumber= %s WHERE name= %s;",(unumber, name))

def find_update():
    message = []
    update = 0
    with SQL_Manager() as sql:
        novel = get_novel(sql)
        for (name, url, unumber) in novel:
            new_content = update_get(url, unumber)
            for (index, chapter, content) in new_content:
                content = HanziConv.toTraditional(content)
                r_str = "{} has new chapter, chapter {}: {}".format(name, chapter, content)
                message.append(r_str)
                update = index
            if update:
                update_unumber(sql, name, update)
    return message

# def sql_init(sql):
#         sql_build()
#         add_novel("逆天邪神", "https://www.piaotian.com/html/6/6760/index.html",index=6499820)
#         add_novel("修真聊天群", "https://www.piaotian.com/html/7/7580/index.html",index=6499820)



if __name__ == '__main__':
    # sql_build()
    # add_novel("逆天邪神", "https://www.piaotian.com/html/6/6760/index.html")
    # add_novel("修真聊天群", "https://www.piaotian.com/html/7/7580/index.html")
    message = find_update()
    for i in message:
        print(i)
    # with SQL_Manager('novel.db') as sql:
    #     update_unumber(sql, "修真聊天群", 6499820)
    #     update_unumber(sql, "逆天邪神", 6478632)
    # if os.path.isfile("./Data.db") == False:
    #     pass