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

def getData(sql):
    data = []
    con, cur = getCursor()
    if con == None:
        return None
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        for r in row:
          data.append(r)
    con.close()
    return data


################
## DB 연결부분 ##
################

# 도서 목록 받아오기
def getBookList():
  sql = f"SELECT NAME FROM INFO ORDER BY NAME ASC"
  bookList = getData(sql=sql)
  return bookList

# 해당 도서 마지막권(화) 받아오기
def getLastVolume(bookName):
  sql = f"SELECT MAX(VOLUME) FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')"
  lastVolume = getData(sql)
  return lastVolume[0]

# 해당 도서 모든 권(화) 받아오기
def getVolumes(bookName):
  sql = f"SELECT DISTINCT VOLUME FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')"
  volumeList = getData(sql=sql)
  return volumeList

# 해당 도서 해당 권(화) 내용 받아오기
def getContents(bookName, volume):
  sql = f"SELECT CONTENTS FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME={volume} ORDER BY LINE ASC"
  lineList = getData(sql=sql)
  return lineList

# 관리자 비번 받아오기
def getAdminPw():
  sql = f"SELECT PASSWORD FROM OPTIONS"
  pw = getData(sql=sql)
  return pw[0]
