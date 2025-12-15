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
        data.append(row)
    con.close()
    return data


################
## DB 연결부분 ##
################

# 도서 목록 받아오기
def getBookList():
  sql = f"SELECT * FROM INFO"
  bookList = getData(sql=sql)
  for book in bookList:
     book = book[1]
  print('bookList:',bookList)
  return bookList

# 해당 도서 마지막권(화) 받아오기
def getLastVolume(bookName):
  sql = f"SELECT MAX(VOLUME) FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')"
  lastVolume = getData(sql)
  lastVolume = lastVolume[0]
  print('lastVolume:',lastVolume)
  return lastVolume

# 해당 도서 모든 권(화) 받아오기
def getVolumes(bookName):
  sql = f"SELECT DISTINCT VOLUME FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')"
  volumeList = list(getData(sql=sql))
  for volume in volumeList:
     volume = volume[0]
  print('volumeList:',volumeList)
  return volumeList

# 해당 도서 해당 권(화) 내용 받아오기
def getContents(bookName, volume):
  sql = f"SELECT CONTENTS FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME={volume} ORDER BY LINE ASC"
  lineList = list(getData(sql=sql))
  for line in lineList:
     line = line[0]
  print('lineList:',lineList)
  return lineList

# 관리자 비번 받아오기
def getAdminPw():
  sql = f"SELECT PASSWORD FROM OPTIONS"
  pw = getData(sql=sql)
  pw = pw[0][0]
  print('pw:',pw)
  return pw
