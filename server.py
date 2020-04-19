import socket
import select

def send_to_all(sock, message):
	for socket in connected_list:
		if socket != server_socket and socket != sock:
			try:
				socket.send(bytes(message, 'utf-8'))
			except:
				socket.close()
				connected_list.remove(socket)

name = ""
record = {}
connected_list = []
buffer = 2048
port = 10000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", port))
server_socket.listen(10)

connected_list.append(server_socket)

print("\u001b[32m\u001b[1m\t\t\t\t\tSERVER WORKING\u001b[0m")

while 1:
	rList, wList, errList = select.select(connected_list, [], [])
	for sock in rList:
		if sock == server_socket:
			sockid, addr = server_socket.accept()
			name = sockid.recv(buffer).decode('utf-8')
			connected_list.append(sockid)
			record[addr] = ""

			if name in record.values():
				sockid.send(bytes("\r\u001b[31m\u001b[1mUsername already taken!\u001b[0m\n", 'utf-8'))
				del record[addr]
				connected_list.remove(sockid)
				sockid.close()
				continue
			else:
				record[addr] = name
				print("Client connected:" + str(addr) + " [ " + str(record[addr]) + " ]")
				sockid.send(bytes("\r\u001b[32;1m\u001b[1mWelcome to the chat room. Enter 'exit' anytime to exit.\u001b[0m\n", 'utf-8'))
				send_to_all(sockid, "\r\u001b[32;1m\u001b[1m" + str(name) + " joined the conversation\u001b[0m\n")
		else:
			try:
				data1 = sock.recv(buffer).decode('utf-8')
				data = data1[:data1.index("\n")]

				i, p = sock.getpeername()
				if data == "exit":
					msg = "\r\u001b[32;1m\u001b[1m" + str(record[(i, p)]) + " left the conversation\u001b[0m\n"
					send_to_all(sock, msg)
					print("Client " + str((i , p)) + " " + str(record[(i , p)]) + " is offline")
					del record[(i, p)]
					connected_list.remove(sock)
					sock.close()
					continue
				else:
					msg = "\r\u001b[34m\u001b[1m\u001b[1m" + str(record[(i, p)]) + ":\u001b[0m " + str(data + "\n")
					send_to_all(sock, msg)

			except:
				(i, p) = sock.getpeername()
				send_to_all(sock, "\r\u001b[32;1m\u001b[1m" + str(record[(i, p)]) + " left the conversation unexpectedly\u001b[0m\n")
				print("Client: " + str(record[(i, p)]) + " is offline(error)")
				del record[(i, p)]
				connected_list.remove(sock)
				sock.close()
				continue

server_socket.close()