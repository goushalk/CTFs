#!/usr/bin/python3

import re
import sys
import socket
from functools import wraps
from threading import Thread

attempts = 3 
time = 5  
secret = "aHR0cHM6Ly95b3V0dS5iZS9HY1lJSS1XbUdWaz9zaT01LXV6YkZfX0ZUUFBTQzJy"
forbidden_chars = "1234567890!@#$%^&*()_?/\\|`~{}][" 
PORT = 1337

def print_jail():
    jail = r"""
    +------------------------+
    |   ||   ||   ||   ||    |
    |   ||   ||   ||   ||    |
    |   ||   ||   ||   ||    |
    +----++----++----++----+++
    |                        |
    |     Mathiya Serai      |
    |        (Jail)          |
    +------------------------+
    """
    return jail

def clean_input(user_input):
    return re.sub(f"[{re.escape(forbidden_chars)}]", "", user_input, count=3)

def limit_attempts(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(attempts):
            result = func(*args, **kwargs)
            if result:  
                return result
        return "You failed to get out off Mathiya Serai! (Jail)\n"
    return wrapper

@limit_attempts
def challenge(conn):
    flaaaaaaaaaaag = "flag{fakeflag}"
    tmp = "A9DIWENPEJ/5$FF8%ES EYJC//58PC-B9.W5U DS-A/08VDDNW6E%E3JCP2C4+8+6AUNA:G6"
    
    try:
        conn.sendall(b"Vidaamuyarchi sei! Try to breakout from your Mathiya Serai (Jail): ")
        
        conn.settimeout(time)
        inp = conn.recv(1024).decode().strip()
        conn.settimeout(None)  

        cleaned_inp = clean_input(inp)

        if len(cleaned_inp) < 9 and 'flaaaaaaaaaaag' not in cleaned_inp:
            result = str(eval(cleaned_inp)) + "\n"
            conn.sendall(result.encode())
            return result
        else:
            conn.sendall(b"\nAdhula Onnum Illa, Keela Potudu!\n")
            conn.sendall(b"\nThere is nothing there, put down!\n")
            return None
            
    except socket.timeout:
        conn.sendall(b"\nTime Illa!...\n")
        conn.sendall(b"\nNo Time!...\n")
        return None
    except Exception as e:
        conn.sendall(b"\nBoard aduna, Board mattum dha adanam!\n")
        conn.sendall(b"\nOnly Play The GAME!!!\n")
        return None

def handle_client(conn):
    try:
        welcome = "----------------- Welcome to Mathiya Serai (Jail) -----------------\n\n"
        conn.sendall(welcome.encode())
        conn.sendall(print_jail().encode())
        conn.sendall(b"\n")
        challenge(conn)
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', PORT))
    server.listen(5)
    
    print(f"Server listening on port {PORT}")
    
    try:
        while True:
            conn, addr = server.accept()
            print(f"New connection from {addr}")
            client_thread = Thread(target=handle_client, args=(conn,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
