import socket


class Client():
    def __init__(self):
        self.cmd_list = [
            ('help', 'show this description'),
            ('list', 'folders and files list in current directory'),
            ('dwld {FILE_PATH}', 'download file from server'),
            ('pwd', 'show current directory path'),
            ('cd {DIRECTORY_NAME}', 'change the directory'),
            ('exit', 'close the FTP client')
        ]
        self.host = '127.0.0.1'
        self.port = 2121
        self.buffer_size = 1024

    def welcome(self):
        print('Welcome to the FTP client\n')
        print('List of available commands:')
        for cmd, desc in self.cmd_list:
            print(f"{f'{cmd}':<23}{f': {desc}':<40}")

    def main(self):
        self.welcome()


myClient = Client()
myClient.main()
