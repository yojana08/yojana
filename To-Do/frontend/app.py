from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
import pymongo
from pymongo.mongo_client import MongoClient


load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client.test

todos_collection = db['todos']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('todo.html')


@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    if item_name and item_description:
        todos_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

    return redirect('/')

@app.route('/api')
def api():
    todos = list(todos_collection.find({}, {'_id': 0}))
    return {"todos": todos}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)