from flask import Flask, render_template
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

app = Flask(__name__)

@app.route("/")
def main():
  data=db.getData()
  return  render_template('index.html',data=data)

@app.route("/<bookName>")
def selectVolume(bookName):
  bookInfo['name'] = bookName
  volumes = [1,2,3,4,5] # 이거 나중엔 서버에서 받아와야 함
  return render_template('selectVolume.html', bookInfo=bookInfo, volumes=volumes)

if __name__ == '__main__':
  print('############외부ip:',get_external_ip() + '############') # 나중에 지울 예정
  app.run(
    debug=True
    , host='0.0.0.0'
  )
