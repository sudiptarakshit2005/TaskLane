
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

import database

app = FastAPI(title="Tasklane Real-Time Task Manager")

database.create_table()

clients = []


async def send_board():
    tasks = database.all_tasks()

    disconnected = []

    for client in clients:
        try:
            await client.send_json(tasks)
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        if client in clients:
            clients.remove(client)


@app.websocket("/ws")
async def board(websocket: WebSocket):

    await websocket.accept()
    clients.append(websocket)

    await send_board()

    try:
        while True:

            message = await websocket.receive_json()

            action = message.get("action")

            if action == "add":

                title = message.get("title", "").strip()
                person = message.get("person", "").strip()

                if title and person:
                    database.add_task(title, person)

            elif action == "move":

                task_id = message.get("id")
                status = message.get("status")

                if task_id is not None:
                    database.move_task(task_id, status)

            elif action == "delete":

                task_id = message.get("id")

                if task_id is not None:
                    database.delete_task(task_id)

            await send_board()

    except WebSocketDisconnect:

        if websocket in clients:
            clients.remove(websocket)


app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)
