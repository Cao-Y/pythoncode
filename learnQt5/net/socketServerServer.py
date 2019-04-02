import socketserver


class udpServer(socketserver.BaseRequestHandler):
    def handle(self):
        print('服务端启动...')
        conn = self.request
        print(conn)
        print('获得连接：', self.client_address)
        client_data = self.request[0]
        if not client_data:
            print('断开连接')
        print(client_data.decode('utf-8'))
        print('开始发送...')
        self.request[1].sendto(client_data,self.client_address)


if __name__ == '__main__':
    server = socketserver.UDPServer(("127.0.0.1", 8000), udpServer)  # 使用处理单连接的UDPServer
    server.serve_forever()