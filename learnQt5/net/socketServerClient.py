import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    st = input('input command: ')

    s.sendto(st.encode('utf-8'),('127.0.0.1', 8000))

    echo_back,address = s.recvfrom(1024)
    print(address)
    print(echo_back.decode('utf-8'))
    s.close()