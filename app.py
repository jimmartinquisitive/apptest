from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'Hello, Azure App Gateway! Served from: {socket.gethostname()}'

if __name__ == '__main__':
    app.run()
