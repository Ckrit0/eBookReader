import pymysql

dbInfo = {
  'host' : 'localhost',
  'port' : 3306,
  'user' : 'ckrit',
  'password' : 'P@ssw0rd',
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
  try:
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
      for r in row:
        data.append(r)
  except Exception as e:
    print(e)
  finally:
    con.close()
  return data

def setData(sql):
  result = False
  con, cur = getCursor()
  try:
    cur.execute(sql)
    result = cur.fetchall()
    con.commit()
  except Exception as e:
    print(e)
  finally:
    con.close()
  return result


################
## DB 연결부분 ##
################

# 관리자 비번 받아오기
def getAdminPw():
  sql = f"SELECT PASSWORD FROM OPTIONS"
  pw = getData(sql=sql)[0]
  return pw

# 도서 목록 받아오기
def getBookList():
  sql = f"SELECT NAME FROM INFO ORDER BY NAME ASC"
  bookList = getData(sql=sql)
  return bookList

# 해당 도서 마지막권(화) 받아오기
def getLastVolume(bookName):
  sql = f"SELECT IFNULL((SELECT MAX(VOLUME) FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')),0)"
  lastVolume = getData(sql)[0]
  return lastVolume

# 해당 도서 모든 권(화) 받아오기
def getVolumes(bookName):
  sql = f"SELECT DISTINCT VOLUME FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}') ORDER BY VOLUME"
  volumeList = getData(sql=sql)
  return volumeList

# 해당 도서 해당 권(화) 내용 받아오기
def getContents(bookName, volume):
  sql = f"SELECT CONTENTS FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME={volume} ORDER BY LINE ASC"
  lineList = getData(sql=sql)
  return lineList

# 도서 추가하기
def insertBook(bookName):
  sql = f"INSERT INTO INFO VALUES((SELECT IFNULL((SELECT MAX(BID)+1 FROM INFO),0)),'{bookName}')"
  setData(sql=sql)

# 도서명 변경하기
def updateBook(bookName,newName):
  sql = f"UPDATE INFO SET NAME='{newName}' WHERE NAME='{bookName}'"
  setData(sql=sql)

# 도서 삭제하기
def deleteBook(bookName):
  # 내용 삭제
  sql = f"DELETE FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')"
  setData(sql=sql)
  # 도서정보 삭제
  sql = f"DELETE FROM INFO WHERE NAME='{bookName}'"
  setData(sql=sql)

# 볼륨 컨텐츠 추가하기(수정하기)
def insertVolume(bookName,volume,contentList):
  # 기존 내용 삭제
  sql = f"DELETE FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume}"
  setData(sql=sql)
  # 새로운 내용 추가
  sql = f"INSERT INTO CONTENT VALUES("
  for i in range(len(contentList)):
    sql = sql + f"((SELECT BID FROM INFO WHERE NAME='{bookName}'),{volume},{i+1},'{contentList[i]}')"
    if i < len(contentList)-1:
      sql = sql + f", "
  sql = sql + ")"
  setData(sql=sql)

# 볼륨 수정하기
def updateVolume(bookName,volume,newVolume):
  sql = f"UPDATE CONTENT SET VOLUME = {newVolume} WHERE BID = (SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume}"
  setData(sql=sql)

# 볼륨 삭제하기
def deleteVolume(bookName,volume):
  sql = f"DELETE CONTENT WHERE BID = (SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume}"
  setData(sql=sql)

# 라인 수정하기
def updateContent(bookName,volume,line,content):
  sql = f"UPDATE CONTENT SET CONTENT = '{content}' WHERE BID = (SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume} AND LINE = {line}"
  setData(sql=sql)

# 라인 삭제하기
def deleteContent(bookName,volume,line):
  sql = f"DELETE CONTENT WHERE  BID = (SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume} AND LINE = {line}"
  setData(sql=sql)
  # 이후 라인 땡기기
  sql = f"UPDATE CONTENT SET LINE = ((SELECT LINE FROM CONTENT WHERE BID = (SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume} AND LINE = {line}) - 1) WHERE BID = (SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume} AND LINE > {line}"
  setData()
