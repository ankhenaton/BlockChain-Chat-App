import socket

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Send a message to the server
message = input("Enter your message: ")
client_socket.sendall(message.encode('utf-8'))

# Receive the updated chat blockchain from the server
response = client_socket.recv(1024).strip().decode('utf-8')
print("Updated chat blockchain:", response)

# Close the connection
client_socket.close()
