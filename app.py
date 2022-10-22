import queue
from datetime import datetime
from flask import Flask

app = Flask(__name__)

store = {}

def make_err(msg):
    return { 'error': 1, 'msg': msg }
def make_res(data):
    return { 'error': 0, 'data': data }

@app.route('/get', methods=['GET'])
def get():
    item_list = []
    for item_id, queue in store.items():
        if queue.empty():
            continue
        timestamps = list(queue.queue)
        item_list.append({
            'item_id': item_id,
            'count': len(timestamps),
            'timestamps': timestamps,
        })
    return make_res(item_list)

@app.route('/add/<item_id>', methods=['GET'])
def add(item_id):
    if item_id not in store:
        store[item_id] = queue.Queue()
    store[item_id].put(datetime.now())
    return make_res(f'{item_id} is added')

@app.route('/remove/<item_id>', methods=['GET'])
def remove(item_id):
    if item_id in store and not store[item_id].empty():
        store[item_id].get()
    else:
        return make_err('no such item')
    return make_res(f'{item_id} is removed')
