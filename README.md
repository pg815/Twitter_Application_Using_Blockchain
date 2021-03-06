# Twitter_Application_Using_Blockchain

## Install the dependencies,
pip install -r requirements.txt

## To run twitter application,
python run_app.py

## To run multiple nodes in different terminals

### Terminal 1
export FLASK_APP=node_server.py
flask run --port 8000

### Terminal 2
export FLASK_APP=node_server.py
$ flask run --port 8001

### Terminal 3
export FLASK_APP=node_server.py
$ flask run --port 8002

### Terminal 4
#### Register Nodes 8001 and 8002 to 8000,


curl -X POST \
  http://127.0.0.1:8001/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'


  curl -X POST \
  http://127.0.0.1:8002/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
