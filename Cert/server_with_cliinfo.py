"""
참조 : https://blog.naver.com/PostView.nhn?blogId=username1103&logNo=222111281954
"""
import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('svr.crt', 'svr.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind('127.0.0.1', 8443)
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        data = conn.recv(65535)
        print(data)