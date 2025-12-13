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

############## 샘플 ##################
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


################
## DB 연결부분 ##
################

# 도서 목록 받아오기
def getBookList():
  tempBooks = []
  for i in range(10):
    tempBooks.append('Book' + (str(i+1)))
  return tempBooks

# 해당 도서 마지막권(화) 받아오기
def getLastVolume(bookName):
  if bookName == '':
    return 0
  
  return 15

# 해당 도서 모든 권(화) 받아오기
def getVolumes(bookName):
  tempVolume = []
  for i in range(15):
    tempVolume.append(i+1)
  return tempVolume

# 해당 도서 해당 권(화) 내용 받아오기
def getContents(bookName, volume):
  tmpLines = []
  for i in range(100):
    tmpLines.append('line' + (str(i+1)))
  return tmpLines

# 관리자 비번 받아오기
def getAdminPw():
  return 'test'
