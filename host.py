# 관리자모드 세션방식으로 바꿔야 함

from flask import Flask, render_template, request, redirect, url_for
import sqlCRUD as db
import bookQueue

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

bookQ = bookQueue.BookQueue()
bookInfo = initBookInfo()
bookList = db.getBookList()
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
    elif request.form['password'] == db.getAdminPw():
      isAdmin = True
      return render_template('indexAdmin.html', bookList=bookList)
    else:
      return render_template('password.html')

# /admin/도서명
@app.route("/admin/<bookName>")
def selectVolumeAdmin(bookName):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  volumes = db.getVolumes(bookName=bookName)
  return render_template('selectVolumeAdmin.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

# /admin/도서명/권(화)
@app.route("/admin/<bookName>/<volume>")
def viewContentsAdmin(bookName, volume):
  global isAdmin
  if not isAdmin:
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
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=int(volume))
  return redirect(url_for('viewContentsAdmin',bookName=bookName, volume=volume))

# /insert/도서명
@app.route("/insert/<bookName>", methods=['GET'])
def insertContents(bookName):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = db.getLastVolume(bookName=bookName)
  initData()
  return render_template('insertContents.html', bookList=bookList, bookInfo=bookInfo, bookName=bookName)

# /insert/도서명/권(화)
@app.route("/insert/<bookName>/<volume>")
def modifyContents(bookName, volume):
  global isAdmin
  if not isAdmin:
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
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  db.insertBook(bookName=bookName)
  initData()
  return redirect(url_for("admin"))

@app.route("/insert/<bookName>/<volume>",methods=["POST"])
def insertBookContents(bookName,volume):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  contentList = []
  keyList = list(request.form.keys())
  keyList.sort()
  for i in keyList:
    line = request.form[i].strip()
    if line != '':
      contentList.append(request.form[i])
  db.insertVolume(bookName=bookName,volume=volume,contentList=contentList)
  initData()
  return redirect(url_for('viewContentsAdmin',bookName=bookName,volume=volume))

@app.route("/update/<bookName>",methods=["POST"])
def updateBookName(bookName):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  newName = request.form['data']
  db.updateBook(bookName=bookName,newName=newName)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/update/<bookName>/<volume>",methods=["POST"])
def updateBookVolume(bookName,volume):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  newVolume = request.form['data']
  db.updateVolume(bookName=bookName,volume=volume,newVolume=newVolume)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/update/<bookName>/<volume>/<line>/<redLine>",methods=["POST"])
def updateBookContent(bookName,volume,line,redLine):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  content = request.form['data']
  db.updateContent(bookName=bookName,volume=volume,line=line,content=content)
  initData()
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=redLine))

@app.route("/delete/<bookName>",methods=["POST"])
def deleteBookName(bookName):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  db.deleteBook(bookName=bookName)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/delete/<bookName>/<volume>",methods=["POST"])
def deleteBookVolume(bookName,volume):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  db.deleteVolume(bookName=bookName,volume=volume)
  initData()
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/delete/<bookName>/<volume>/<line>",methods=["POST"])
def deleteBookContent(bookName,volume,line):
  global isAdmin
  if not isAdmin:
    return redirect(url_for("password"))
  db.deleteContent(bookName=bookName,volume=volume,line=line)
  initData()
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=line))

if __name__ == '__main__':
  app.run(
    debug=True,
    host='0.0.0.0'
  )
