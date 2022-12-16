import hashlib
import time
import threading
import socketserver

class Block:
    def __init__(self, data, previous_hash):
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()
    
    def calc_hash(self):
        sha = hashlib.sha256()
        hash_str = self.data.encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.lock = threading.Lock()
    
    def add_block(self, data):
        with self.lock:
            if len(self.chain) == 0:
                previous_hash = 0
            else:
                previous_hash = self.chain[-1].hash
            block = Block(data, previous_hash)
            self.chain.append(block)

# Set up the server
chat = Blockchain()

class ChatRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive the message from the client
        message = self.request.recv(1024).strip().decode('utf-8')
        
        # Add the message to the chat blockchain
        chat.add_block(message)
        
        # Send the updated chat blockchain to the client
        self.request.sendall(str(chat.chain).encode('utf-8'))

server = socketserver.ThreadingTCPServer(('localhost', 8000), ChatRequestHandler)
server.serve_forever()
