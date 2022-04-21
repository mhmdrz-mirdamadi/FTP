import socket
import os
import json


class Server():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 2121
        self.buffer_size = 2048
        self.root_path = os.getcwd()
        self.current_path = '/'
        print('Welcome to the FTP server')
        print(f'Server is ready to listen on port {self.port}\n')

    def new_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.connection, self.address = self.socket.accept()
        print(
            f'Server listening to {self.address[0]} from port {self.address[1]}\n')

    def list(self):
        buffer = '\n'
        total_size = 0
        files_list = os.listdir()
        if self.current_path == '/':
            files_list.remove('server.py')
        for file in files_list:
            file_size = os.path.getsize(file)
            file_path = f"\t{f'{file}':<25}{f'{file_size} bytes':<20}\n"
            if os.path.isdir(file):
                file_path = '>' + file_path
            total_size += file_size
            buffer += file_path
        buffer += f"\n\t{f'Total size':<25}{f'{total_size} bytes':<20}\n"
        self.connection.send(buffer.encode())

    def pwd(self):
        self.connection.send(self.current_path.encode())

    def cd(self, path):
        path = [dir for dir in path if dir not in ['', '.']]
        buffer = dict()
        buffer['cd'] = False
        buffer['dir'] = self.current_path
        if path[0] == '..' and self.current_path == '/':
            buffer['msg'] = 'Access Denied!'
            return buffer
        dir = os.getcwd() + '/' + '/'.join(path)
        if not os.path.isdir(dir):
            buffer['msg'] = 'Directory not found!'
            return buffer
        os.chdir(dir)
        self.current_path = os.getcwd()[len(self.root_path):]
        if len(self.current_path) == 0:
            self.current_path = '/'
        buffer['cd'] = True
        buffer['msg'] = 'Directory changed successfully.'
        buffer['dir'] = self.current_path
        return buffer

    def exit(self):
        self.connection.close()
        print(
            f'Client {self.address[0]} from port {self.address[1]} disconnected')
        print(f'Server is ready to listen on port {self.port}\n')

    def main(self):
        while True:
            self.new_connection()
            while True:
                print('- Waiting for command ...')
                cmd = self.connection.recv(self.buffer_size).decode()
                if cmd.lower() == 'help':
                    print('Command: help\n')
                elif cmd.lower() == 'list':
                    print('Command: list')
                    self.list()
                    print('Successfuly sent list of files\n')
                elif cmd.lower().startswith('dwld ') and len(cmd) > 5:
                    pass
                elif cmd.lower() == 'pwd':
                    print('Command: pwd\n')
                    self.pwd()
                elif cmd.lower().startswith('cd ') and len(cmd) > 3:
                    print('Command: cd')
                    print(f'Requested path: {cmd[3:]}')
                    buffer = self.cd(cmd[3:].split('/'))
                    print(buffer['msg'])
                    print(f'Current directory: {buffer["dir"]}\n')
                    self.connection.send(json.dumps(buffer).encode())
                elif cmd.lower() == 'exit':
                    print('Command: exit\n')
                    self.exit()
                    break
                else:
                    if len(cmd) == 0:
                        continue
                    print(f"Invalid command '{cmd}' Received!\n")


myServer = Server()
myServer.main()
