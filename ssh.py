import argparse
import threading
import socket
import sys
import traceback
import paramiko
import subprocess

log = open("logs/log.txt", "a")
HOST_KEY = paramiko.RSAKey(filename='keys/private.key')


def attackerInterac(command, chan):
    response = ""
    if command.startswith("ls"):
        response = "Desktop   Downloads   text.txt"
    elif command.startswith("pwd"):
        response = "/root"
    elif command.startswith("whoami"):
        response = "root"
    elif command == "help":
        return
    else:
        response = command + ": command not found"
    chan.send(response + "\r\n")
    log.write(response + "\n")
    log.flush()
 
class SSHoneywall(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
	if(username == 'root') and (password  == 'password123'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


def sshconnection(client, addr):
    log.write("\n\nConnection from: " + addr[0] + "\n")
    log.write(addr[0] +" execution steps: "+ "\n")
    print(addr[0] +" execution steps: "+ "\n")
    subprocess.call(['sudo', './sshblock.sh', addr[0]])
    print('Blocked ip : '+addr[0])
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        server = SSHoneywall()
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            print('* SSH negotiation failed.')
            raise Exception("SSH negotiation failed")
        # wait for auth
        chan = transport.accept(20)
        if chan is None:
            print('* No channel.')
            raise Exception("No channel")

        server.event.wait(10)
        if not server.event.is_set():
            print('* Client never asked for a shell.')
            raise Exception("No shell request")

        try:
            chan.send("Welcome to Ubuntu 16.04.7 LTS (GNU/Linux 4.15.0-142-generic i686)\r\n\r\n* Documentation:  https://help.ubuntu.com\r\n* Management: https://landscape.canonical.com\r\n* Support: https://ubuntu.com/advantage\n\r\n")
            chan.send("UA Infra: Extended Security Maintenance (ESM) is not enabled.\r\n\r\n0 updates can be applied immediately.\r\n\r\n160 additional security updates can be applied with UA Infra: ESM\r\nLearn more about enabling UA Infra: ESM service for Ubuntu 16.04 at\r\nhttps://ubuntu.com/16-04")
            chan.send("\r\nUbuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by\r\napplicable law.\r\n\r\nLast login: Sun Apr 10 12:45:40 2022 from 10.0.2.5\r\n")  
	    flag = True
            while flag:
                chan.send("$ ")
                command = ""
                while not command.endswith("\r"):
                    transport = chan.recv(1024)
                    chan.send(transport)
                    command += transport.decode("utf-8")

                chan.send("\r\n")
                command = command.rstrip()
                log.write("$ " + command + "\n")
                print(command)
                if command == "exit":
                    flag = False
                else:
                    attackerInterac(command, chan)

        except Exception as err:
            print('!!! Exception: {}: {}'.format(err._class_, err))
            traceback.print_exc()
            try:
                transport.close()
            except Exception:
                pass

        chan.close()

    except Exception as err:
        print('!!! Exception: {}: {}'.format(err._class_, err))
        traceback.print_exc()
        try:
            transport.close()
        except Exception:
            pass


def start_server(port, bind):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        print('* Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        try:
            sock.listen(100)
            print('Listening for connection ...')
            client, addr = sock.accept()
        except Exception as err:
            print('* Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=sshconnection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)

    #for thread in threads:
    #    thread.join()


if _name_ == "_main_":
    parser = argparse.ArgumentParser(description='Run a fake ssh server')
    parser.add_argument("--port", "-p", help="The port to bind the ssh server to (default 22)", default=22, type=int, action="store")
    parser.add_argument("--bind", "-b", help="The address to bind the ssh server to", default="", type=str, action="store")
    args = parser.parse_args()
    start_server(args.port, args.bind)