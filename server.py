import socket
from datetime import datetime
from os.path import join, isfile
from threading import Thread
from settings import *


def add_log(date, addr, path):
    with open('log.txt', 'a') as logs:
        logs.write(f'<{date}> {addr}: {path}\n')


def read_file(path):
    return open(path, 'rb').read()


def generate_path(request):
    path = request.split('\n')[0].split(' ')[1][1:]
    if not path:
        path = DEFAULT_PATH
    return join(DIRECTORY, path)


def get_extension(path):
    return path.split('.')[-1]


def get_code(path, extension):
    if not isfile(path):
        return 404
    elif extension not in ALLOWED_TYPES:
        return 403
    else:
        return 200


def get_date():
    return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')


def process(request, addr):
    path = generate_path(request)
    extension = get_extension(path)
    code = get_code(path, extension)
    date = get_date()
    body = b''
    if code == 200:
        body = read_file(path)
    else:
        extension = 'html'
    response = RESPONSE_PATTERN.format(code, CODES[code], date, TYPES[extension], len(body)).encode() + body
    add_log(date, addr, path)
    return response


def handle(conn: socket.socket, addr):
    with conn:
        request = conn.recv(BUFFER_SIZE).decode()
        print(request)
        if request:
            print(request)
            response = process(request, addr)
            conn.send(response)


def accept(sock):
    while True:
        conn, addr = sock.accept()
        print(f'Подключен {addr}')
        Thread(target=handle, args=[conn, addr]).start()


def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    print((HOST, PORT))
    sock.listen(10)
    accept(sock)


if __name__ == '__main__':
    main()
