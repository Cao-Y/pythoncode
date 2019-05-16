import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
st = input('input command: ')
while True:


    s.sendto(st.encode('utf-8'),('169.254.212.137', 8000))

    echo_back,address = s.recvfrom(1024)
    print(address)
    print(echo_back.decode('utf-8'))
    #s.close()