import pymysql

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'uniquestudio',
    'db': 'user',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


def register(username, password):
    connection = pymysql.connect(**config)
    c = connection.cursor()
    sql = "select * from user where username=%s"
    c.execute(sql, (username))
    results = c.fetchall()
    if not results:
        sql = "insert into user values(%s,%s)"
        c.execute(sql, (username, password))
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False


def login(username, password):
    connection = pymysql.connect(**config)
    c = connection.cursor()
    sql = "select * from user where username=%s"
    c.execute(sql, (username))
    results = c.fetchall()
    connection.close()
    if not results:
        return -1
    elif results[0]['password'] == password:
        return 1
    else:
        return 0

# def get_info(user):
#     return info
#
# def get_list(word=None,tag=None,keyword=None):
#     return user
#
# def get_detail(videoID):
#     return detail
