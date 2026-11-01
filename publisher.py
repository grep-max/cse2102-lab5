import os

from flask import Flask, request, jsonify


# Define the Flask app
app = Flask(__name__)

# All subscribers are stored in the publisher: name -> URI
subscribers = {}
subject = ""

@app.route('/')
def home():
  return "Hello from Flask!"


# curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice","URI":"http://good.site.com"}' http://localhost:5000/add-subscriber

@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():
  data = request.get_json(silent=True) or {}
  name = data.get('name')
  URI = data.get('URI')
  if not name or not URI:
    return jsonify({'error': 'Both "name" and "URI" are required'}), 400
  subscribers[name] = URI
  print(f"You entered: Name={name}, Address={URI}")
  return jsonify({'message': f'You sent name: {name} and address: {URI}'}), 201


# curl -X DELETE -H "Content-Type: application/json" -d '{"name":"Alice"}' http://localhost:5000/delete-subscriber

@app.route('/delete-subscriber', methods=['DELETE'])
def deleteSubscriber():
  data = request.get_json(silent=True) or {}
  name = data.get('name')
  if not name:
    return jsonify({'error': '"name" is required'}), 400
  if name not in subscribers:
    print(f"Delete failed: no subscriber named {name}")
    return jsonify({'error': f'No subscriber named {name}'}), 404
  URI = subscribers.pop(name)
  print(f"You deleted: Name={name}, Address={URI}")
  return jsonify({'message': f'You deleted subscriber: {name}'})


# curl http://localhost:5000/list-subscribers

@app.route('/list-subscribers', methods=['GET'])
def listSubscribers():
  print("Current subscribers:")
  for key in subscribers.keys():
    print(f"  {key} at {subscribers[key]}")
  return jsonify({'subscribers': subscribers})


# curl -X POST -H "Content-Type: application/json" -d '{"subject-update":"buy IBM"}' http://localhost:5000/update-and-notify

@app.route('/update-and-notify', methods=['POST'])
def updateAndNotifyAllSubscribers():
  global subject
  data = request.get_json(silent=True) or {}
  newSubject = data.get('subject-update')
  if newSubject is None:
    return jsonify({'error': '"subject-update" is required'}), 400
  subject = newSubject
  print(f"You updated the subject to: {subject}")
  notified = []
  for key in subscribers.keys():
    print(f"Notifying {key} at {subscribers[key]} of the new subject: {subject}")
    notified.append(key)
  return jsonify({'message': f'You updated subject to: {subject} ', 'notified': notified})


@app.route('/subject', methods=['GET'])
def getSubject():
  return jsonify({'subject': subject})

if __name__ == '__main__':
  # Port 5000 is taken by AirPlay on macOS, so allow overriding it: PORT=5055 python publisher.py
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
