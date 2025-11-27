import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'Whffkaos1!',
    'database' : 'E_BOOK_READER'
}

def getCursor():
    global dbInfo
    con = None
    cur = None
    try:
        con = pymysql.connect(
            host=dbInfo['host'],
            port=dbInfo['port'],
            user=dbInfo['user'],
            password=dbInfo['password'],
            database=dbInfo['database']
        )
        cur = con.cursor()
    except Exception as e:
        print('Connect Error:',e)
    return con, cur

def getData():
    data = []
    sql='SELECT * FROM CONTENT'
    con, cur = getCursor()
    if con == None:
        return None
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        data.append(row)
    con.close()
    return data

print(getData())
