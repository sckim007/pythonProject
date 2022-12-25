"""
참조 : https://blog.naver.com/PostView.nhn?blogId=username1103&logNo=222111281954
"""
import socket
import ssl

hostname = 'www.pss.com'
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('CA.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        ssock.connect(('localhost'), 8443)
        ssock.send(b'hello')