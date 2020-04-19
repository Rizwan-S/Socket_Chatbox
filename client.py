import socket, select, string, sys

def display():
	sys.stdout.write("\u001b[36m\u001b[1mYou: \u001b[0m")
	sys.stdout.flush()

port = 10000

name = str(input("\u001b[33;1m\u001b[1mCREATING NEW ID:\nEnter username: \u001b[0m"))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

try :
    s.connect(("127.0.0.1", port))
except :
    print("\u001b[31m\u001b[1mCan't connect to the server\u001b[0m")
    sys.exit()

s.send(bytes(name, 'utf-8'))
display()
while 1:
    socket_list = [sys.stdin, s]
    rList, wList, error_list = select.select(socket_list , [], [])
    for sock in rList:
        if sock == s:
            data = sock.recv(2048).decode('utf-8')
            if not data :
                print("\u001b[31m\u001b[1mDISCONNECTED\u001b[0m")
                sys.exit()
            else :
                sys.stdout.write(data)
                display()
        else :
            msg=sys.stdin.readline()
            s.send(bytes(msg, 'utf-8'))
            display()

