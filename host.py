from flask import Flask, render_template, request, redirect, url_for
import sqlCRUD as db
import bookQueue
import requests

def get_external_ip(): # 나중에 지울 예정
  try:
    response = requests.get('https://api.ipify.org')
    external_ip = response.text
    return external_ip
  except Exception as e:
    print('Error: ',e)
    return 'ip_check_error'

def initBookInfo(): # bookInfo 초기화
  bookInfo = {
    'name' : '',
    'volume' : 0,
    'line' : bookQ.getLine(),
    'lastVolume' : getLastVolume(),
  }
  return bookInfo

def getLastVolume(): # 임시값. 서버에서 받아와야 함.
  return 5

def getContents():
  return ['line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line','line'] # 임시값. 서버에서 받아와야 함
  
# 변수 모음
bookQ = bookQueue.BookQueue()
bookInfo = initBookInfo()
bookList = ['t1','te2','tes3','test4','testt5','testte6','testtes7','testtest8'] # 임시값. 서버에서 받아와야함.
adminPw = "test"
isAdmin = False

app = Flask(__name__)

@app.route("/")
def main():
  return  render_template('index.html', bookList=bookList)

@app.route("/<bookName>")
def selectVolume(bookName):
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  bookInfo['lastVolume'] = getLastVolume()
  volumes = [1,2,3,4,5] # 임시값. 서버에서 받아와야 함
  return render_template('selectVolume.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

@app.route("/<bookName>/<volume>")
def viewContents(bookName, volume):
  lastVolume = getLastVolume()
  bookInfo = initBookInfo()
  bookInfo['name'] = bookName
  try :
    if int(volume) > lastVolume:
      volume = lastVolume
    bookInfo['volume'] = int(volume)
  except :
    bookInfo['volume'] = bookQ.getVolume()
  bookInfo['lastVolume'] = getLastVolume()
  contents = getContents()
  return render_template('contents.html', bookList=bookList, bookInfo=bookInfo, contents = contents)

@app.route("/<bookName>/<volume>/<line>")
def viewContentsForLine(bookName, volume, line):
  bookQ.setLine(line=line)
  bookQ.setVolume(volume=volume)
  return redirect(url_for('viewContents',bookName=bookName, volume=volume))

@app.route("/admin",methods=["GET"])
def password():
    global isAdmin
    if isAdmin:
      return render_template('admin.html', bookList=bookList)
    else:
      return render_template('password.html')

@app.route("/admin",methods=["POST"])
def admin():
    global isAdmin
    if isAdmin:
      return render_template('admin.html', bookList=bookList)
    elif request.form['password'] == adminPw:
      isAdmin = True
      return render_template('admin.html', bookList=bookList)
    else:
      return render_template('password.html')
      
  

if __name__ == '__main__':
  print('############외부ip:',get_external_ip() + '############') # 나중에 지울 예정
  app.run(
    debug=True
    , host='0.0.0.0'
  )
