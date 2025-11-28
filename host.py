from flask import Flask, render_template, request
import sqlCRUD as db
import requests

def get_external_ip(): # 나중에 지울 예정
  try:
    response = requests.get('https://api.ipify.org')
    external_ip = response.text
    return external_ip
  except Exception as e:
    print('Error: ',e)
    return 'ip_check_error'
  
# 변수 모음
bookInfo = {
  'name' : '',
  'value' : 0,
  'line' : 0
}
bookList = ['test1','test2','test3'] # 임시값. 서버에서 받아와야함.
adminPw = "test"
isAdmin = False

app = Flask(__name__)

@app.route("/")
def main():
  return  render_template('index.html', bookList=bookList)

@app.route("/<bookName>")
def selectVolume(bookName):
  bookInfo['name'] = bookName
  volumes = [1,2,3,4,5] # 임시값. 서버에서 받아와야 함
  return render_template('selectVolume.html', bookList=bookList, bookInfo=bookInfo, volumes=volumes)

@app.route("/<bookName>/<volume>")
def viewContents(bookName, volume):
  data=db.getData()
  bookInfo['name'] = bookName
  bookInfo['volume'] = int(volume)
  contents = ['line1','line2','line3'] # 임시값. 서버에서 받아와야 함
  return render_template('contents.html', bookList=bookList, bookInfo=bookInfo, contents = contents)

@app.route("/admin",methods=["GET"])
def password():
    if isAdmin:
      admin()
    else:
      return render_template('password.html')

@app.route("/admin",methods=["POST"])
def admin():
    if isAdmin:
      return render_template('admin.html', bookList=bookList)
    elif request.form['password'] == adminPw:
      isAdmin = True
      return render_template('admin.html', bookList=bookList)
    else:
      password()
      
  

if __name__ == '__main__':
  print('############외부ip:',get_external_ip() + '############') # 나중에 지울 예정
  app.run(
    debug=True
    , host='0.0.0.0'
  )
