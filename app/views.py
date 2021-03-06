import datetime
import json
from users import Users
import os.path

import requests
from flask import render_template, redirect, request,jsonify,flash, session

from app import app
app.secret_key = "sdfgskcv"
# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/posts')
def index():
    fetch_posts()
    return render_template('posts.html',
                           title='YourNet: Decentralized '
                                 'content sharing',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')    

@app.route('/login', methods=['POST'])
def login():
    user = Users()
    srno = 0
    username = request.form["username"]
    password = request.form["password"]
    srno = user.getUser(username,password)
    result = "asdf"
    if srno == 0:
        flash("User Not available !!")
        print("Not a user")
        return render_template('index.html',scroll = 'about')
    else:
        session['username'] = username
        print("allowed posts")
        return redirect('/posts')

@app.route('/signup')
def signUp():
    return render_template('signup.html')
    
@app.route('/register', methods=['POST'])
def register():
    username = request.form["username"]
    password = request.form["password"]
    user = Users()
    user.createUser(username,password)
    return render_template('index.html',scroll = 'about')


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = session['username']
    image = request.files['file']
    if image :  
        path  = os.path.join("app/static/Images",author)
        if os.path.isdir(path):
               image.save(path + "/" + image.filename)
               img_filename = image.filename
               img_path = os.path.join("static/Images/" + author ,img_filename)
               print(img_path)
        else:
            os.mkdir(path)
            image.save(path + "/" + image.filename)
            img_filename = image.filename
            img_path = os.path.join("static/Images/" + author ,img_filename)
            print(img_path)
        
        post_object = {
        'author': author,
        'content': post_content,
        'image' : img_path,
        }
     
        print(post_content)
        print(author)
    
    else :
        post_object = {
        'author': author,
        'content': post_content,
        'image' : "img",
        }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/posts')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
