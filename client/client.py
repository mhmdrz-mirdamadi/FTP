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
        self.help()

    def help(self):
        print('List of available commands:')
        for cmd, desc in self.cmd_list:
            print(f"{f'{cmd}':<23}{f': {desc}':<40}")

    def main(self):
        self.welcome()
        while True:
            cmd = input('> ')
            if cmd not in [_[0] for _ in self.cmd_list]:
                print("Invalid command! See 'help' for list of available commands.")
                continue
            elif cmd.lower() == 'help':
                self.help()
            elif cmd.lower() == 'list':
                pass
            elif cmd.lower().startswith('dwld'):
                pass
            elif cmd.lower() == 'pwd':
                pass
            elif cmd.lower().startswith('cd'):
                pass
            else:
                break


myClient = Client()
myClient.main()
