from flask import Flask, jsonify, redirect, request, url_for
from flask.templating import render_template
from flask_pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.todo_db
todos = db.todos


@app.route("/basic")
def home():
    return render_template("index.html")


@app.route("/post", methods=['POST', 'GET'])
def add_data():
    title = request.form.get('tname')
    desc = request.form.get('desc')
    db.todos.insert_one({'title': title, 'desc': desc})
    return redirect(url_for('get_data'))


@app.route('/get', methods=['POST', 'GET'])
def get_data():
    todis = todos.find()
    return render_template("index.html", todo=todis)


@app.route('/update_one/<did>')
def upd_one(did):
    todo = todos.find({"_id": ObjectId(f"{did}")})
    return render_template('update.html', todos=todo)


@app.route('/update_two/<did>', methods=['POST'])
def upd_two(did):
    title = request.form.get('tname')
    desc = request.form.get('dname')
    if title != "":
        todos.update_one({"_id": ObjectId(f"{did}")}, {
            "$set": {"title": title}})
    elif desc != "":
        todos.update_one({"_id": ObjectId(f"{did}")}, {
            "$set": {"desc": desc}})
    return redirect(url_for('get_data'))


@app.route('/remove_all')
def del_all():
    todos.delete_many({})
    return redirect(url_for('home'))


@app.route('/remove_one/<did>')
def del_one(did):
    todos.delete_one({"_id": ObjectId(f"{did}")})
    return redirect(url_for('get_data'))


if __name__ == "__main__":
    app.run(debug=False)
