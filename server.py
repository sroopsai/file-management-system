"""[module-docstring]
"""

import asyncio
import signal
import socket
from commandhandler import CommandHandler

signal.signal(signal.SIGINT, signal.SIG_DFL)

def client_request(commandhandler, message):
    """
    This function initiates the functions for given commands by user
    """
    command = message.rstrip("\n").rstrip(" ").lstrip(" ").split(" ")[0]
    if command == "commands":
        return commandhandler.commands()
    if command == "register":
        if len(message.split(" ")) == 3:
            return commandhandler.register(message.split(" ")[1], message.split(" ")[2])
        return "Enter correct command"

    if command == "login":
        if len(message.split(" ")) == 3:
            return commandhandler.login(message.split(" ")[1], message.split(" ")[2])
        return "Enter Right Command"

    if command == "quit":
        return commandhandler.quit()

    if command == "create_folder":
        if len(message.split(" ")) == 2:
            return commandhandler.create_folder(message.split(" ")[1])
        return "Enter correct command: command --> create_folder <folder-name>"

    if command == "change_folder":
        if len(message.split(" ")) == 2:
            return commandhandler.change_folder(message.split(" ")[1])
        return "Enter correct command: command --> change_folder <folder-name>"

    if command == "write_file":
        if len(message.split(" ")) >= 2:
            return commandhandler.write_file(message.split(" ")[1], " ".join(message.split(" ")[2:]))
        return "Enter correct command: command -> write_file <file_name> <content>"

    if command == "read_file":
        if len(message.split(" ")) >= 2:
            return commandhandler.read_file(message.split(" ")[1])
        return "Enter correct command: command -> read_file <file_name>"

    if command == "list":
        return commandhandler.list()

async def handle_client(reader, writer):
    """This funtion acknowledges the connection from the client,
    acknowledges the messages from the client
    Parameters
    ----------
    reader : StreamReader
        Reads data from the client socket
    writer : StreamWriter
        Writes data to the client socket
    """

    client_addr = writer.get_extra_info('peername')
    message = f"{client_addr} is connected !!!!"
    print(message)
    commandhandler = CommandHandler()
    while True:
        data = await reader.read(4096)
        message = data.decode().strip()
        if message == 'exit':
            break

        print(f"Received {message} from {client_addr}")
        writer.write(str(client_request(commandhandler, message)).encode())
        await writer.drain()
    print("Close the connection")
    writer.close()


async def main():
    """This function starts the connection between the server and client
    """
    
    server = await asyncio.start_server(handle_client, socket.gethostbyname(socket.gethostname()), 8088)
    server_listening_ip = server.sockets[0].getsockname()
    print(f'Serving on {server_listening_ip}')
    async with server:
        await server.serve_forever()


asyncio.run(main())
