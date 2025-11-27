from flask import Flask
import sqlCRUD as db

app = Flask(__name__)

@app.route("/")
def main():
  data=db.getData()
  return  data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
