from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import pymongo
from pymongo.mongo_client import MongoClient


load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client.test

collection = db['flask']


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)





app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():

   form_data = dict(request.json)
   collection.insert_one(form_data)

   return "Data Submitted Successfully"

@app.route('/view')
def view():

    data = collection.find()

    data = list(data)
    for item in data:
        print(item)

        del item['_id']
    
    data = {
        'data': data
    }

    return jsonify(data)

@app.route('/api')
def name():

    return jsonify({
        "message": "Updated API content from Tutedude_new branch",
        "author": "Tutedude",
        "status": "active"
    })


if __name__=='__main__':
    app.run(host = '0.0.0.0', port=9000,debug=True)

