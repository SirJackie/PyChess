import socket


class JSock:
    debug = None
    mode = None
    s = None
    clientSocket = None

    def __init__(self, debug_=True):
        self.debug = debug_
        # Create Socket Object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Enable Port Reuse
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def StartServer(self, port, maxConnections=32):
        self.mode = "Server"
        self.s.bind(("127.0.0.1", port))
        self.s.listen(maxConnections)
        if self.debug:
            print(f"Server Started at Port: {port}")

    def AcceptClient(self):
        if self.mode != "Server":
            raise Exception("You're trying to accept a client using a client socket.")
        self.clientSocket, address = self.s.accept()
        if self.debug:
            print(f"Client Accepted: {address}")

    def SendStr(self, msgStr):
        if self.mode == "Server":
            s = self.clientSocket
        else:
            s = self.s
        s.send(f"{len(msgStr):<10}".encode("utf-8"))
        s.send(msgStr.encode("utf-8"))

    def RecvStr(self):
        if self.mode == "Server":
            s = self.clientSocket
        else:
            s = self.s
        msgLen = int(s.recv(10).decode("utf-8").strip())
        return s.recv(msgLen).decode("utf-8")

    def Connect(self, ip, port):
        self.mode = "Client"
        while True:
            try:
                if self.debug:
                    print(f"Connecting: ({ip}, {port})")
                self.s.connect((ip, port))
                break
            except ConnectionRefusedError:
                if self.debug:
                    print("Failed to Connect, Reconnecting...")

    def Close(self):
        if self.mode == "Server":
            self.clientSocket.close()
        else:
            self.s.close()
