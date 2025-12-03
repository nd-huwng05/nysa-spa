from app import new_server

server = new_server()
app = server.app

if __name__ == '__main__':
    server.start()