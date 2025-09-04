
# Simple RAT made with Python

---

**Disclaimer: *This project is not made for any malicious purpose.***

## About this project

This is a simple RAT (Remote Access Trojan). A RAT is a kind of trojan horse malware which is used to gain remote access of another computer.  
After executing the **victim.py** script it will behave like gui calculator in the foreground but in the background it will send the access to the attacker computer. it is cross platform means this will work on both windows and linux based systems.

## Usage

* **Step 1:**

---

Change the value of the **host** in both attacker and victim script with the ip or domain of the attacker machine.
You can change the value of the **port** with any port which is not well known or registered.

* **Step 2:**

---

Run the **attacker.py** file, it will listen and wait for the connection.

* **Step 3:**

---

Send the **victim.py** file to the machine you want to compromise (for testing purpose).

Then after executing the **victim.py** file you will get remote connection from the victim machine.

## Custom commands
There are 2 custom commands in this script

1. **The get command:**  
If you want to transfer any file from the victim machine you can use the get command.
just write the get and the file name or full path without quotation.  
**Syntax:** get <FILE_NAME or PATH>

2. **The chbuff command:**  
if you want modify the receiving buffer in the run time you can do that by using chbuff command.
just write chbuff and the buffer size in bytes by default it is set to 1048576 bytes or 1 mb.  
**Syntax**: chbuff <BUFFER_SIZE in bytes>

## Other details

1. **Converting into exe:**  
You can convert the **victim.py** into an windows executable or exe file using other tool or python packages like **pyinstaller**.  
To install pyinstaller run: `pip install pyinstaller`  
To convert into exe run: `pyinstaller victim.py --onefile --noconsole`  
Then send the exe file to the victim machine.

2. **Working over the internet:**  
If you want to get the remote access of a machine which is on the internet you can do this by using any tunnelling service like **ngrok**.  
Just paste the tunnel link in the **host** value and the tunnel port number in the **port** value.
