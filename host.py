from flask import Flask, render_template, request, redirect, url_for
import sqlCRUD as db
import bookQueue
import requests


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
  
  return 5

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

# bookInfo 초기화
def initBookInfo():
  bookInfo = {
    'name' : '',
    'volume' : 0,
    'line' : bookQ.getLine(),
    'lastVolume' : getLastVolume(''),
  }
  return bookInfo

bookQ = bookQueue.BookQueue()
bookInfo = initBookInfo()
bookList = getBookList()
isAdmin = False


#######################
## Flask 웹 서버 부분 ##
#######################

app = Flask(__name__)

# /
@app.route("/")
def main():
  return  render_template('index.html', bookList=bookList)

# /도서명
@app.route("/read/<bookName>")
def selectVolume(bookName):
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = getLastVolume(bookName=bookName)
  volumes = getVolumes(bookName=bookName)
  return render_template('selectVolume.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

# /도서명/권(화)
@app.route("/read/<bookName>/<volume>")
def viewContents(bookName, volume):
  lastVolume = getLastVolume(bookName=bookName)
  try :
    volume = int(volume)
  except :
    volume = bookQ.getVolume()
  if volume > lastVolume:
    return redirect(url_for('viewContents',bookName=bookName,volume=volume))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['volume'] = volume
  bookInfo['lastVolume'] = lastVolume
  contents = getContents(bookName=bookName,volume=volume)
  return render_template('contents.html', bookList=bookList, bookInfo=bookInfo, contents = contents)

# /도서명/권(화)/줄
@app.route("/read/<bookName>/<volume>/<line>")
def viewContentsForLine(bookName, volume, line):
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=int(volume))
  return redirect(url_for('viewContents',bookName=bookName, volume=volume))


# /admin GET
@app.route("/admin",methods=["GET"])
def password():
    global isAdmin
    if isAdmin:
      return render_template('indexAdmin.html', bookList=bookList)
    else:
      return render_template('password.html')

# /admin POST
@app.route("/admin",methods=["POST"])
def admin():
    global isAdmin
    if isAdmin:
      return render_template('admin.html', bookList=bookList)
    elif request.form['password'] == getAdminPw():
      isAdmin = True
      return render_template('indexAdmin.html', bookList=bookList)
    else:
      return render_template('password.html')

# /admin/도서명
@app.route("/admin/<bookName>")
def selectVolumeAdmin(bookName):
  global isAdmin
  if not isAdmin:
    return redirect(url_for(password()))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = getLastVolume(bookName=bookName)
  volumes = getVolumes(bookName=bookName)
  return render_template('selectVolumeAdmin.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

# /admin/도서명/권(화)
@app.route("/admin/<bookName>/<volume>")
def viewContentsAdmin(bookName, volume):
  global isAdmin
  if not isAdmin:
    return redirect(url_for(password()))
  lastVolume = getLastVolume(bookName=bookName)
  try :
    volume = int(volume)
  except :
    volume = bookQ.getVolume()
  if volume > lastVolume:
    return redirect(url_for('viewContents',bookName=bookName,volume=volume))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['volume'] = volume
  bookInfo['lastVolume'] = lastVolume
  contents = getContents(bookName=bookName,volume=volume)
  return render_template('contentsAdmin.html', bookList=bookList, bookInfo=bookInfo, contents = contents)

# /admin/도서명/권(화)/줄
@app.route("/admin/<bookName>/<volume>/<line>")
def viewContentsForLineAdmin(bookName, volume, line):
  global isAdmin
  if not isAdmin:
    return redirect(url_for(password()))
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=int(volume))
  return redirect(url_for('viewContentsAdmin',bookName=bookName, volume=volume))


      
  

if __name__ == '__main__':
  app.run(
    host='0.0.0.0'
  )
