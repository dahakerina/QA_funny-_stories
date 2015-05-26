#!flask/bin/python
import libvirt
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import url_for
from flask import request
import sys
from xml.etree.ElementTree import fromstring
import subprocess
import pika
import time
import sqlite3

listUser = []


def log_in(log, pas):
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute("select password from author where login = '" + str(log) + "'")

    for row in cur:
        if row[0] != pas:
            return 0
    cur.execute("select id, login from author where login = '" + str(log) + \
                    "' and password = '" + str(pas) + "'")

    for row in cur:
        listUser.append(row[0])
        listUser.append(row[1])
        return 1


def get_authorID():
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute("select max(id) from author")

    for row in cur:
        if row[0] is not None:
            return row[0] + 1

    return 1


def get_storyID():
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute("select max(id) from stories")

    for row in cur:
        if row[0] is not None:
            return row[0] + 1

    return 1


def repeatSearch(login):
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute("select login from author where login = '" + str(login) + "'")
    for row in cur:
        if row[0] is not None:
            return 0
    return 1


def addAutor(login, password):
    if repeatSearch(login):
        ID = get_authorID()
        con = sqlite3.connect('pik.db')
        cur = con.cursor()
        strInsert = "insert into author values" + \
                        str((ID, login, password, 0)) + ";"
        cur.execute(strInsert)
        con.commit()
        return "OK"

    else:
        return "error! login exists"


def createStory(name, body):
    ID = get_storyID()
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    strInsert = "insert into stories values" + \
                    str((ID, name, body, listUser[0], 0)) + ";"
    cur.execute(strInsert)
    con.commit()


def listStories():
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM stories')
    listStory = []

    for row in cur:
        i = 'ID: ' + str(row[0])
        name = 'Story name: ' + row[1]
        body = 'Story body: ' + row[2]
        author = 'Author: ' + str(row[3])
        rating = 'Rating: ' + str(row[4])
        listStory.append([i, name, body, author, rating])

    return listStory


def listStoriesRating(r):
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM stories where rating >= ' + str(r))
    listStory = []

    for row in cur:
        i = 'ID: ' + str(row[0])
        name = 'Story name: ' + row[1]
        body = 'Story body: ' + row[2]
        author = 'Author: ' + str(row[3])
        rating = 'Rating: ' + str(row[4])
        listStory.append([i, name, body, author, rating])

    return listStory


def listStoriesID(id1):
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM stories where id = ' + str(id1))

    for row in cur:
        i = 'ID: ' + str(row[0])
        name = 'Story name: ' + row[1]
        body = 'Story body: ' + row[2]
        author = 'Author: ' + str(row[3])
        rating = 'Rating: ' + str(row[4])
        return [i, name, body, author, rating]

    return 1


def listStoriesAuthor(nameA):
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute('SELECT id FROM author where login = "' + nameA + '"')
    id1 = -1
    for row in cur:
        id1 = row[0]
    if id1 == -1:
        return 1

    cur.execute('SELECT * FROM stories where author = ' + str(id1))
    listStory = []

    for row in cur:
        i = 'ID: ' + str(row[0])
        name = 'Story name: ' + row[1]
        body = 'Story body: ' + row[2]
        author = 'Author: ' + str(row[3])
        rating = 'Rating: ' + str(row[4])
        listStory.append([i, name, body, author, rating])
    return listStory


def likeID(i):
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute('UPDATE stories SET rating = rating + 1 where ID =' + str(i))
    con.commit()


def dislikeID(i):
    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute('UPDATE stories SET rating = rating - 1 where ID =' + str(i))
    con.commit()


def delStory(i):
    author = listStoriesID(i)
    au = author[3].split(" ")
    print au[-1], listUser[0]

    if int(au[-1]) != listUser[0]:
        return 1

    con = sqlite3.connect('pik.db')
    cur = con.cursor()
    cur.execute('delete from stories where ID =' + str(i))
    con.commit()
    return 'OK'


app = Flask(__name__)


#get a list of all stories
@app.route('/list_all/', methods=['GET'])
def get_list_all():
    return jsonify({'stories': listStories()})


#get a list of story id
@app.route('/story_id/<int:id1>', methods=['GET'])
def get_list_id(id1):
    return jsonify({'stories': listStoriesID(id1)})


#get a list of story author
@app.route('/author_story/<string:name>', methods=['GET'])
def get_list_name(name):
    result = listStoriesAuthor(name)
    if result != 1:
        return jsonify({'stories': result})
    else:
        return jsonify({'error': 'the author does not exist'})


#get a list of all the stories with a rating > r
@app.route('/list_rating/<int:r>', methods=['GET'])
def get_list_rating(r):
    return jsonify({'stories': listStoriesRating(r)})


#add story
@app.route('/add_story', methods=['POST'])
def create_story():
    if listUser == []:
        return jsonify({'error': 'log in!!!'})
    story = request.json
    createStory(story.get('name'), story.get('body'))
    return jsonify({story.get('name'): story.get('body')})


#like story
@app.route('/like/<int:i>', methods=['GET'])
def get_like_ID(i):
    exist = listStoriesID(i)

    if exist == 1:
        return jsonify({'error': 'this story does not exist'})

    likeID(i)
    return jsonify({'stories': listStoriesID(i)})


#dislike story
@app.route('/dislike/<int:i>', methods=['GET'])
def get_dislike_ID(i):
    exist = listStoriesID(i)

    if exist == 1:
        return jsonify({'error': 'this story does not exist'})

    dislikeID(i)
    return jsonify({'stories': listStoriesID(i)})


#registration
@app.route('/registration', methods=['POST'])
def reg_author():
    autor = request.json
    l = autor.get('log')
    p = autor.get('pass')
    get_authorID()
    result = addAutor(l, p)
    if result == "OK":
        log_in(l, p)
    return jsonify({l: result})


#log in
@app.route('/log_in', methods=['POST'])
def log_author():
    if listUser == []:
        autor = request.json
        authorID = log_in(autor.get('log'), autor.get('pass'))

        if authorID == 0:
            return jsonify({'error': 'invalid password'})

        if listUser != []:
            return jsonify({autor.get('log'): "OK"})

        return jsonify({autor.get('log'): "registration?"})
    return jsonify({'error': 'log out!'})


#log out
@app.route('/log_out', methods=['GET'])
def log_out():
    if listUser != []:
        name = str(listUser[1])
        i = str(listUser[0])
        listUser.remove(name)
        listUser.remove(int(i))
        return jsonify({name: 'log out'})
    return jsonify({'error': 'log in!'})


#delete story
@app.route('/delete/<int:i>', methods=['GET'])
def del_story(i):
    if listUser == []:
        return jsonify({'error': 'log in!'})

    exist = listStoriesID(i)
    if exist == 1:
        return jsonify({'error': 'this story does not exist'})

    result = delStory(i)
    if result == 1:
        return jsonify({'error': 'Only an author can delete the story'})
    return jsonify({'story': result})


if __name__ == '__main__':
    con = sqlite3.connect('pik.db')
    cur = con.cursor()

    try:
        cur.execute("""CREATE TABLE stories (
                       id PRIMARY KEY,
                       name,
                       body,
                       author,
                       rating );
                    """)

        cur.execute("""CREATE TABLE author (
                       id PRIMARY KEY,
                       login,
                       password,
                       rating );
                    """)

        con.commit()
    except:
        pass
    app.run(debug=True)
