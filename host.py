from flask import Flask
import sqlCRUD as db
import requests

def get_external_ip():
  try:
    response = requests.get('https://api.ipify.org')
    external_ip = response.text
    return external_ip
  except Exception as e:
    print('Error: ',e)
    return 'ip_check_error'

app = Flask(__name__)

@app.route("/")
def main():
  data=db.getData()
  result = ""
  for row in data:
    result = result + data
  return  result

if __name__ == '__main__':
  print('############외부ip:',get_external_ip() + '############')
  app.run(
    debug=True
    , host='0.0.0.0'
  )









