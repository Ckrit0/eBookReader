from flask import Flask, render_template, request, redirect, url_for
import sqlCRUD as db
import bookQueue
from datetime import datetime, timedelta
import pytz

sessionTime = 1 # 세션의 적용시간(hour)

def initData():
  global bookInfo, bookList, bookQ
  bookInfo = initBookInfo()
  bookList = db.getBookList()
  bookQ = bookQueue.BookQueue()

def initBookInfo():
  bookInfo = {
    'name' : '',
    'volume' : 0,
    'line' : bookQ.getLine(),
    'lastVolume' : db.getLastVolume(''),
  }
  return bookInfo

def setAdmin(userId):
  global session
  session[userId] = userId
  session['setTime' + userId] = datetime.now(tz=pytz.timezone('Asia/Seoul')) + timedelta(hours=sessionTime)

def isAdmin(userId):
  global session
  result = False
  try:
    sessionId = session[userId]
    setTime = session['setTime' + sessionId]
    now = datetime.now(tz=pytz.timezone('Asia/Seoul'))
    if now > setTime:
      session.pop(sessionId)
      session.pop('setTime' + sessionId)
    else:
      setAdmin(userId=userId)
      result = True
  except Exception as e:
    print(e)
    return False
  return result

bookQ = bookQueue.BookQueue()
bookInfo = initBookInfo()
bookList = db.getBookList()
session = {}
app = Flask(__name__)

@app.route("/")
def main():
  return render_template('index.html', bookList=bookList)

@app.route("/read/<bookName>")
def selectVolume(bookName):
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  volumes = db.getVolumes(bookName=bookName)
  return render_template('selectVolume.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

@app.route("/read/<bookName>/<volume>")
def viewContents(bookName, volume):
  lastVolume = db.getLastVolume(bookName=bookName)
  try :
    volume = int(volume)
  except :
    volume = bookQ.getVolume()
  if volume > lastVolume:
    return redirect(url_for('viewContents',bookName=bookName,volume=lastVolume))
  elif volume < 1:
    return redirect(url_for('viewContents',bookName=bookName,volume=1))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['volume'] = volume
  bookInfo['lastVolume'] = lastVolume
  contents = db.getContents(bookName=bookName,volume=volume)
  return render_template('contents.html', bookList=bookList, bookInfo=bookInfo, contents=contents)

@app.route("/read/<bookName>/<volume>/<line>")
def viewContentsForLine(bookName, volume, line):
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=int(volume))
  return redirect(url_for('viewContents',bookName=bookName, volume=volume))

@app.route("/admin",methods=["GET"])
def password():
    if not isAdmin(request.remote_addr):
      return render_template('password.html')
    else:
      return render_template('indexAdmin.html', bookList=bookList)

@app.route("/admin",methods=["POST"])
def admin():
    if request.form['password'] == db.getAdminPw():
      setAdmin(request.remote_addr)
    return redirect(url_for("password"))

@app.route("/admin/<bookName>")
def selectVolumeAdmin(bookName):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  volumes = db.getVolumes(bookName=bookName)
  return render_template('selectVolumeAdmin.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

@app.route("/admin/<bookName>/<volume>")
def viewContentsAdmin(bookName, volume):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  lastVolume = db.getLastVolume(bookName=bookName)
  try :
    volume = int(volume)
  except :
    volume = bookQ.getVolume()
  if volume > lastVolume:
    return redirect(url_for('viewContentsAdmin',bookName=bookName,volume=lastVolume))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['volume'] = volume
  bookInfo['lastVolume'] = lastVolume
  contents = db.getContents(bookName=bookName,volume=volume)
  return render_template('contentsAdmin.html', bookList=bookList, bookInfo=bookInfo, contents = contents)

@app.route("/admin/<bookName>/<volume>/<line>")
def viewContentsForLineAdmin(bookName, volume, line):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=int(volume))
  return redirect(url_for('viewContentsAdmin',bookName=bookName, volume=volume))

@app.route("/insert/<bookName>", methods=['GET'])
def insertContents(bookName):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  initData()
  return render_template('insertContents.html', bookList=bookList, bookInfo=bookInfo, bookName=bookName)

@app.route("/insert/<bookName>/<volume>")
def modifyContents(bookName, volume):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['volume'] = volume
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  contents = ""
  tempContents = db.getContents(bookName=bookName,volume=volume)
  for content in tempContents:
    contents = contents + content + "\n"
  contents = contents.rstrip('\n')
  return render_template('insertContents.html',bookList=bookList,bookInfo=bookInfo,bookName=bookName,contents=contents)

@app.route("/insert/<bookName>",methods=["POST"])
def insertBookName(bookName):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.insertBook(bookName=bookName)
  initData()
  return redirect(url_for("admin"))

@app.route("/insert/<bookName>/<volume>",methods=["POST"])
def insertBookContents(bookName,volume):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  contentDict = {}
  for key in request.form.keys():
    contentDict[key] = request.form[key]
  result, bookId = bookQ.setContents(contentDict=contentDict)
  contents = bookQ.getContents(bookId=bookId)
  if result >= 100:
    print('완료율:',result,'%')
    db.insertVolume(bookName=bookName, volume=volume, contents=contents)
    initData()
    return redirect(url_for('viewContentsAdmin',bookName=bookName,volume=volume))
  else :
    print('완료율:',result,'%')
    return str(result) + "%"

@app.route("/update/<bookName>",methods=["POST"])
def updateBookName(bookName):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  newName = request.form['data']
  db.updateBook(bookName=bookName,newName=newName)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/update/<bookName>/<volume>",methods=["POST"])
def updateBookVolume(bookName,volume):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  newVolume = request.form['data']
  db.updateVolume(bookName=bookName,volume=volume,newVolume=newVolume)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/update/<bookName>/<volume>/<line>/<redLine>",methods=["POST"])
def updateBookContent(bookName,volume,line,redLine):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  content = request.form['data']
  db.updateContent(bookName=bookName,volume=volume,line=line,content=content)
  initData()
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=redLine))

@app.route("/delete/<bookName>",methods=["POST"])
def deleteBookName(bookName):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.deleteBook(bookName=bookName)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/delete/<bookName>/<volume>",methods=["POST"])
def deleteBookVolume(bookName,volume):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.deleteVolume(bookName=bookName,volume=volume)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/delete/<bookName>/<volume>/<line>",methods=["POST"])
def deleteBookContent(bookName,volume,line):
  if not isAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.deleteContent(bookName=bookName,volume=volume,line=line)
  initData()
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=line))

if __name__ == '__main__':
  app.run(
    debug=True,
    host='0.0.0.0'
  )
