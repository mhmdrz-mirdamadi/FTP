import socket
import json


class Client():
    def __init__(self):
        self.cmd_list = [
            ('help', 'show this description'),
            ('list', 'folders and files list in current directory'),
            ('dwld {FILE_NAME}', 'download file from server'),
            ('pwd', 'show current directory path'),
            ('cd {DIRECTORY_NAME}', 'change the directory'),
            ('exit', 'close the FTP client')
        ]
        self.host = '127.0.0.1'
        self.port = 2121
        self.buffer_size = 2048
        self.current_path = '/'

    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def welcome(self):
        print('Welcome to the FTP client\n')
        self.help()

    def help(self):
        print('List of available commands:')
        for cmd, desc in self.cmd_list:
            print(f"{f'{cmd}':<23}{f': {desc}':<40}")

    def list(self):
        print(self.socket.recv(self.buffer_size).decode())

    def dwld(self):
        dwld_res = json.loads(self.socket.recv(self.buffer_size).decode())
        if not dwld_res['dwld']:
            print(dwld_res['msg'])
            return
        dwld_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dwld_client.connect((self.host, dwld_res['port']))
        with open(dwld_res['file_name'], 'wb') as dwld_file:
            data = b''
            while True:
                temp = dwld_client.recv(self.buffer_size)
                if not temp:
                    break
                data += temp
            dwld_file.write(data)
        dwld_client.close()
        print(f"Downloaded '{dwld_res['file_name']}' successfully")

    def pwd(self):
        path = self.socket.recv(self.buffer_size).decode()
        self.current_path = path
        print(f'Current path: {self.current_path}')

    def cd(self):
        cd_res = json.loads(self.socket.recv(self.buffer_size).decode())
        if cd_res['cd']:
            self.current_path = cd_res['dir']
            return
        print(cd_res['msg'])

    def exit(self):
        self.socket.close()

    def main(self):
        self.connect_to_server()
        self.welcome()
        print()
        while True:
            cmd = input(f'{self.current_path}> ')
            if len(cmd) != 0:
                self.socket.send(cmd.encode())
            if cmd.lower() == 'help':
                self.help()
            elif cmd.lower() == 'list':
                self.list()
            elif cmd.lower().startswith('dwld ') and len(cmd) > 5:
                self.dwld()
            elif cmd.lower() == 'pwd':
                self.pwd()
            elif cmd.lower().startswith('cd ') and len(cmd) > 3:
                self.cd()
            elif cmd.lower() == 'exit':
                self.exit()
                break
            else:
                print(
                    f"Invalid command '{cmd}'! See 'help' for list of available commands.")


myClient = Client()
myClient.main()
