import pymysql
mysql_user=""
mysql_password=""

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': mysql_user,
    'password': mysql_password,
    'db': 'user',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

config_girl = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': mysql_user,
    'password': mysql_password,
    'db': 'girl',
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


def commit_girl(username, info):
    connection = pymysql.connect(**config_girl)
    c = connection.cursor()
    sql = "select * from girl where username=%s"
    c.execute(sql, (username))
    results = c.fetchall()
    for i in results:
        if i['girlName'] == info['girlName']:
            return -1
    sql = "insert into girl value(%s,%s,%s,%s,%s,%s,%s)"
    tags = ""
    for i in info["tags"]:
        tags += i + '/'
    c.execute(sql, (username, info['girlName'], info['age'], info['birthday'], info['hometown'], tags, "0"))
    connection.commit()
    connection.close()
    return 1


def change_girl(username, girlName, flag):
    connection = pymysql.connect(**config_girl)
    c = connection.cursor()
    sql = "update girl set flag=%s where username=%s and girlName=%s"
    c.execute(sql, (flag, username, girlName))
    connection.commit()
    connection.close()
    return True


def pull_girl(username):
    connection = pymysql.connect(**config_girl)
    c = connection.cursor()
    sql = "select * from girl where username=%s"
    c.execute(sql, (username))
    results = c.fetchall()
    connection.close()
    return results


def get_tags(username, girlName):
    connection = pymysql.connect(**config_girl)
    c = connection.cursor()
    sql = "select * from girl where username=%s and girlName=%s"
    c.execute(sql, (username, girlName))
    results = c.fetchall()
    connection.close()
    return results[0]['tags']
