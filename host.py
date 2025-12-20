from flask import Flask, render_template, request, redirect, url_for, session
import sqlCRUD as db
import bookQueue
from datetime import datetime, timedelta

# 설정용 변수
sessionTime = 1 # 세션의 적용시간(hour)

# 수정 후 데이터 초기화
def initData():
  global bookInfo, bookList, bookQ
  bookInfo = initBookInfo()
  bookList = db.getBookList()
  bookQ = bookQueue.BookQueue()

# bookInfo 초기화
def initBookInfo():
  bookInfo = {
    'name' : '',
    'volume' : 0,
    'line' : bookQ.getLine(),
    'lastVolume' : db.getLastVolume(''),
  }
  return bookInfo

# admin session 추가
def setAdmin(userId):
  session[userId] = userId
  session['setTime' + userId] = datetime.now() + timedelta(hours=sessionTime)

# admin session 확인
def getAdmin(userId):
  now = datetime.now()
  userId = session.get(userId)
  setTime = session.get('setTime' + userId)
  if userId == None:
    return False
  elif now > setTime: # 요청한 id가 유효시간 초과시, 세션 제거
    session.pop(userId)
    session.pop('setTime' + userId)
    return False
  else: # admin을 확인하면 session 시간 초기화
    setAdmin(userId=userId)
    return True

bookQ = bookQueue.BookQueue()
bookInfo = initBookInfo()
bookList = db.getBookList()



#######################
## Flask 웹 서버 부분 ##
#######################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKeyIsCkritKey'

# /
@app.route("/")
def main():
  return render_template('index.html', bookList=bookList)

# /도서명
@app.route("/read/<bookName>")
def selectVolume(bookName):
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  volumes = db.getVolumes(bookName=bookName)
  return render_template('selectVolume.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

# /도서명/권(화)
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

# /도서명/권(화)/줄
@app.route("/read/<bookName>/<volume>/<line>")
def viewContentsForLine(bookName, volume, line):
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=int(volume))
  return redirect(url_for('viewContents',bookName=bookName, volume=volume))


# /admin GET
@app.route("/admin",methods=["GET"])
def password():
    if getAdmin(request.remote_addr):
      return render_template('indexAdmin.html', bookList=bookList)
    else:
      return render_template('password.html')

# /admin POST
@app.route("/admin",methods=["POST"])
def admin():
    if getAdmin(request.remote_addr):
      return render_template('admin.html', bookList=bookList)
    elif request.form['password'] == db.getAdminPw():
      setAdmin(request.remote_addr)
      return render_template('indexAdmin.html', bookList=bookList)
    else:
      return render_template('password.html')

# /admin/도서명
@app.route("/admin/<bookName>")
def selectVolumeAdmin(bookName):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  volumes = db.getVolumes(bookName=bookName)
  return render_template('selectVolumeAdmin.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

# /admin/도서명/권(화)
@app.route("/admin/<bookName>/<volume>")
def viewContentsAdmin(bookName, volume):
  if getAdmin(request.remote_addr):
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

# /admin/도서명/권(화)/줄
@app.route("/admin/<bookName>/<volume>/<line>")
def viewContentsForLineAdmin(bookName, volume, line):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=int(volume))
  return redirect(url_for('viewContentsAdmin',bookName=bookName, volume=volume))

# /insert/도서명
@app.route("/insert/<bookName>", methods=['GET'])
def insertContents(bookName):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  initData()
  return render_template('insertContents.html', bookList=bookList, bookInfo=bookInfo, bookName=bookName)

# /insert/도서명/권(화)
@app.route("/insert/<bookName>/<volume>")
def modifyContents(bookName, volume):
  if getAdmin(request.remote_addr):
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
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.insertBook(bookName=bookName)
  initData()
  return redirect(url_for("admin"))

@app.route("/insert/<bookName>/<volume>",methods=["POST"])
def insertBookContents(bookName,volume):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  contentDict = {}
  for key in request.form.keys():
    contentDict[key] = request.form[key]
  result, bookId = bookQ.setContents(contentDict=contentDict)
  contents = bookQ.getContents(bookId=bookId)
  if result >= 100:
    db.insertVolume(bookName=bookName, volume=volume, contents=contents)
    initData()
    return redirect(url_for('viewContentsAdmin',bookName=bookName,volume=volume))
  else :
    return str(result) + "%"


@app.route("/update/<bookName>",methods=["POST"])
def updateBookName(bookName):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  newName = request.form['data']
  db.updateBook(bookName=bookName,newName=newName)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/update/<bookName>/<volume>",methods=["POST"])
def updateBookVolume(bookName,volume):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  newVolume = request.form['data']
  db.updateVolume(bookName=bookName,volume=volume,newVolume=newVolume)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/update/<bookName>/<volume>/<line>/<redLine>",methods=["POST"])
def updateBookContent(bookName,volume,line,redLine):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  content = request.form['data']
  db.updateContent(bookName=bookName,volume=volume,line=line,content=content)
  initData()
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=redLine))

@app.route("/delete/<bookName>",methods=["POST"])
def deleteBookName(bookName):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.deleteBook(bookName=bookName)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/delete/<bookName>/<volume>",methods=["POST"])
def deleteBookVolume(bookName,volume):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.deleteVolume(bookName=bookName,volume=volume)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/delete/<bookName>/<volume>/<line>",methods=["POST"])
def deleteBookContent(bookName,volume,line):
  if getAdmin(request.remote_addr):
    return redirect(url_for("password"))
  db.deleteContent(bookName=bookName,volume=volume,line=line)
  initData()
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=line))

if __name__ == '__main__':
  app.run(
    debug=True,
    host='0.0.0.0'
  )
