import socket


class Server():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 2121
        self.buffer_size = 2048
        print('Welcome to the FTP server')
        print(f'Server is ready to listen on port {self.port}\n')

    def new_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.connection, self.address = self.socket.accept()
        print(
            f'Server listening to {self.address[0]} from port {self.address[1]}\n')

    def exit(self):
        self.connection.close()

    def main(self):
        self.new_connection()
        while True:
            print('- Waiting for command ...')
            cmd = self.connection.recv(self.buffer_size).decode()
            if cmd.lower() == 'help':
                print('Command: help\n')
            elif cmd.lower() == 'list':
                pass
            elif cmd.lower().startswith('dwld '):
                pass
            elif cmd.lower() == 'pwd':
                pass
            elif cmd.lower().startswith('cd '):
                pass
            elif cmd.lower() == 'exit':
                print('Command: exit\n')
                self.exit()
                break
            else:
                print(f"Invalid command '{cmd}' Received!\n")


myServer = Server()
myServer.main()
