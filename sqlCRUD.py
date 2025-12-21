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

def setDatas(sqlList):
  result = False
  con, cur = getCursor()
  try:
    for sql in sqlList:
      cur.execute(sql)
    result = cur.fetchall()
    con.commit()
  except Exception as e:
    print(e)
  finally:
    con.close()
  return result

def getAdminPw():
  sql = f"SELECT PASSWORD FROM OPTIONS"
  pw = getData(sql=sql)[0]
  return pw

def getBookList():
  sql = f"SELECT NAME FROM INFO ORDER BY NAME ASC"
  bookList = getData(sql=sql)
  return bookList

def getLastVolume(bookName):
  sql = f'''SELECT IFNULL((SELECT MAX(VOLUME)
    FROM CONTENT
    WHERE
      BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')),0)'''
  lastVolume = getData(sql)[0]
  return lastVolume

def getVolumes(bookName):
  sql = f'''SELECT DISTINCT VOLUME
    FROM CONTENT
    WHERE
      BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')
    ORDER BY VOLUME'''
  volumeList = getData(sql=sql)
  return volumeList

def getContents(bookName, volume):
  sql = f'''SELECT CONTENTS
    FROM CONTENT
    WHERE
      BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')
      AND VOLUME={volume}
    ORDER BY LINE ASC'''
  lineList = getData(sql=sql)
  return lineList

def insertBook(bookName):
  sql = f'''INSERT INTO INFO
    VALUES(
      (SELECT IFNULL((SELECT MAX(BID)+1 FROM INFO),0)),
      '{bookName}'
    )'''
  setData(sql=sql)

def updateBook(bookName,newName):
  sql = f"UPDATE INFO SET NAME='{newName}' WHERE NAME='{bookName}'"
  setData(sql=sql)

def deleteBook(bookName):
  sql = f"DELETE FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}')"
  setData(sql=sql)
  sql = f"DELETE FROM INFO WHERE NAME='{bookName}'"
  setData(sql=sql)

def insertVolume(bookName,volume,contents):
  sqlList = []
  deleteSql = f"DELETE FROM CONTENT WHERE BID=(SELECT BID FROM INFO WHERE NAME='{bookName}') AND VOLUME = {volume}"
  sqlList.append(deleteSql)
  keyList = contents.keys()
  insertSql = f""
  for i in keyList:
    insertSql = f'''INSERT INTO CONTENT
      VALUES(
        (SELECT BID FROM INFO WHERE NAME='{bookName}'),{volume},{int(i)+1},'{contents[i]}'
      )'''
    sqlList.append(insertSql)
  setDatas(sqlList=sqlList)

def updateVolume(bookName,volume,newVolume):
  sql = f'''UPDATE CONTENT
    SET VOLUME = {newVolume}
    WHERE
      BID = (SELECT BID FROM INFO WHERE NAME='{bookName}')
      AND VOLUME = {volume}'''
  setData(sql=sql)

def deleteVolume(bookName,volume):
  sql = f'''DELETE FROM CONTENT
    WHERE
      BID = (SELECT BID FROM INFO WHERE NAME='{bookName}')
      AND VOLUME = {volume}'''
  setData(sql=sql)

def updateContent(bookName,volume,line,content):
  sql = f'''UPDATE CONTENT
    SET CONTENTS = '{content}' 
    WHERE
      BID = (SELECT BID FROM INFO WHERE NAME='{bookName}')
      AND VOLUME = {volume}
      AND LINE = {line}'''
  setData(sql=sql)

def deleteContent(bookName,volume,line):
  sqlList = []
  deleteSql = f'''DELETE FROM CONTENT
    WHERE
      BID = (SELECT BID FROM INFO WHERE NAME='{bookName}')
      AND VOLUME = {volume}
      AND LINE = {line}'''
  sqlList.append(deleteSql)
  updateLineNumberSql = f'''UPDATE CONTENT
    SET LINE = (
      (SELECT LINE
      FROM CONTENT
      WHERE
        BID = (SELECT BID FROM INFO WHERE NAME='{bookName}')
        AND VOLUME = {volume}
        AND LINE = {line}) - 1)
    WHERE
      BID = (SELECT BID FROM INFO WHERE NAME='{bookName}')
      AND VOLUME = {volume}
      AND LINE > {line}'''
  sqlList.append(updateLineNumberSql)
  setDatas(sqlList=sqlList)
