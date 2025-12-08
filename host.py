from flask import Flask, render_template, request, redirect, url_for
import sqlCRUD as db
import bookQueue

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
    return redirect(url_for('viewContents',bookName=bookName,volume=volume))
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['volume'] = volume
  bookInfo['lastVolume'] = lastVolume
  contents = db.getContents(bookName=bookName,volume=volume)
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
    return redirect(url_for(password()))
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
    return redirect(url_for(password()))
  lastVolume = db.getLastVolume(bookName=bookName)
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
  contents = db.getContents(bookName=bookName,volume=volume)
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

############################ 기능 미구현 ########################################
@app.route("/insert/<bookName>",methods=["POST"])
def insertBookName(bookName):
  pass

@app.route("/insert/<bookName>/<volume>/<contents>",methods=["POST"])
def insertBookContents(bookName,volume,contents):
  pass

@app.route("/update/<bookName>",methods=["POST"])
def updateBookName(bookName):
  pass

@app.route("/update/<bookName>/<volume>",methods=["POST"])
def updateBookVolume(bookName,volume):
  newVolume = request.form['newVolume']
  print('nowVol:',volume,', newVol:',newVolume)
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/update/<bookName>/<volume>/<contents>",methods=["POST"])
def updateBookContents(bookName,volume,contents):
  pass

@app.route("/update/<bookName>/<volume>/<line>/<redLine>",methods=["POST"])
def updateBookContent(bookName,volume,line,redLine):
  content = request.form['content']
# db에 content로 line update 해야함.
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=redLine))

@app.route("/delete/<bookName>",methods=["POST"])
def deleteBookName(bookName):
  pass

@app.route("/delete/<bookName>/<volume>",methods=["POST"])
def deleteBookVolume(bookName,volume):
  #db 볼륨 삭제, 볼륨들 땡겨서 순서 맞추기
  return redirect(url_for('selectVolumeAdmin',bookName=bookName))

@app.route("/delete/<bookName>/<volume>/<line>",methods=["POST"])
def deleteBookContent(bookName,volume,line):
# db에 line delete해야함. (근데 이거 그럼 라인 정렬 다시 해야하는건데..)
  return redirect(url_for('viewContentsForLineAdmin',bookName=bookName,volume=volume,line=line))




  

if __name__ == '__main__':
  app.run(
    debug=True,
    host='0.0.0.0'
  )
