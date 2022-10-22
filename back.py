import queue
from datetime import datetime

from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

store = {}

def make_err(msg):
    return { 'error': 1, 'msg': msg }
def make_res(data):
    return { 'error': 0, 'data': data }

@app.websocket('/get')
async def endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
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
        await websocket.send_json(make_res(item_list))
        await asyncio.sleep(0.5)

@app.get('/add/{item_id}')
def add(item_id):
    if item_id not in store:
        store[item_id] = queue.Queue()
    store[item_id].put(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return make_res(f'{item_id} is added')

@app.get('/remove/{item_id}')
def remove(item_id):
    if item_id in store and not store[item_id].empty():
        store[item_id].get()
    else:
        return make_err('no such item')
    return make_res(f'{item_id} is removed')
