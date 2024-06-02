from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import subprocess
from random import shuffle
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

app = Flask(__name__)
socketio = SocketIO(app)
# run_with_ngrok(app, auth_token="1rir3uYeUnvI0JqAuwOYhR2z4Tj_4b3qWc6LygfMJjmwQ6ZbW")


def get_shells(result: dict, is_random=False) -> list:
    if is_random:
        result = [f"..\static\png\\{'live'}.png"] * result["lives"] + \
               [f"..\static\png\\{'blank'}.png"] * result["blanks"]
        shuffle(result)
        return result
    else:
        return [f"..\static\png\\{'live'}.png"] * result["lives"] + \
                [f"..\static\png\\{'blank'}.png"] * result["blanks"]


@app.route('/')
def player():
    with open("static/files/refresh/data.json") as file:
        result = json.load(file)
    general = result["general"]
    extra = result["extra"]
    return render_template('index.html',
                           error=request.args,
                           general=general,
                           extra=extra,
                           len=general["shells"],
                           shells=get_shells(general),
                           shells_extra=get_shells(extra),
                           game=result["game"],
                           role="Стать дилером")


@app.route('/restart', methods=['POST'])
def restart():
    proc = subprocess.Popen(['python', 'generator.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line = proc.communicate()[0].decode()
    result = json.loads(line)
    with open("static/files/refresh/data.json", 'w') as file:
        json.dump(result, file)
        # value = request.form["restart_button"]
    socketio.emit('refresh')
    # if value == "Стать игроком":
    #     return redirect(url_for('dealer'))
    # else:
    #     return redirect(url_for('player'))


@app.route('/dealer')
def dealer():
    with open("static/files/refresh/data.json") as file:
        result = json.load(file)
    general = result["general"]
    extra = result["extra"]
    return render_template('index.html',
                           general=general,
                           extra=extra,
                           len=general["shells"],
                           shells=get_shells(general, True),
                           shells_extra=get_shells(extra, True),
                           game=result["game"],
                           role="Стать игроком")


@app.route('/change_role', methods=['POST'])
def change_role():
    value = request.form["change_button"]
    if value == "Стать игроком":
        with open("static/files/users.json", 'w') as file:
            json.dump({"dealer": False}, file)
        return redirect(url_for('player'))
    else:
        with open("static/files/users.json") as file:
            data = json.load(file)
        is_dealer = data["dealer"]
        if is_dealer:
            return redirect(url_for('player', error=data))
        else:
            with open("static/files/users.json", 'w') as file:
                json.dump({"dealer": True}, file)
            return redirect(url_for('dealer'))


class FileCallback(FileSystemEventHandler):
    _counter: int

    def __init__(self):
        self._counter = 0

    def on_modified(self, event):
        self._counter += 1
        if self._counter == 2:
            self._counter = 0

    def on_created(self, event):
        print(f'event type: {event.event_type} path : {event.src_path}')

    def on_deleted(self, event):
        print(f'event type: {event.event_type} path : {event.src_path}')


if __name__ == '__main__':
    event_handler = FileCallback()
    observer = Observer()
    observer.schedule(event_handler, path='static\\files\\refresh', recursive=False)
    # observer.start()

    socketio.run(app, port=8080, allow_unsafe_werkzeug=True)
    # observer.stop()



