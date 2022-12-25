"""
개요
    asyncio를 이용한 소켓 통신을 어떤식으로 구현하는지 살펴보고
    간단한 비동기 다중 접속 에코 서버/클라이언트를 구현하는 과정
빌딩블럭
    비동기 소켓통신을 지원하기 위해 고수준 읽기/쓰기 API를 갖추고 있는 Reader/Writer 객체를 제공
스트림 리더 : asyncio.StreamReader는 IO 스트림에서 데이터를 읽는 API를 제공하는 객체
    read(n=-1)
        최대 n바이트를 읽어 들인다.  n이 -1이면 EOF까지 읽은 다음, 모든 바이트를 반환한다.
        이미 EOF를 수신했고고 내부 버퍼가 비어 있다면 빈 bytes를 반환한다.
    readline()
        개행(\n)으로 구분되는 한 줄을 읽는다.
        EOF를 수신했고 개행을 찾을 수 없으면 남은 데이터를 반환한다.
    readexactly(n)
        정확히 n바이트를 읽는다.
        read와 달리 n 바이트를 읽기 전에 EOF에 도달하면 IncompleteReadError 예외를 일으킨다.
    readuntil(separator=b'\n')
        구분자까지 읽어서 반환한다.(구분자를 포함하여 리턴)
        read와 달리 파일 끝에서 구분자가 발견되지 않으면 IncompleteReadError가 발생하며, 버퍼가 리셋된다.
    at_eof()
        버퍼가 비었고 EOF에 도달하였는지를 검사한다.

스트림 라이터 : IO 스트림에 대해 비동기로 바이트를 쓰는 API를 제공
    write(data)
        하부 스트림에 즉시 data를 기록한다.  실패하는 경우 data를 보낼수 있을 때까지 버퍼에 남는다.
        이는 실제 쓰기 완료를 보장하지 않으므로 '즉시 버퍼에 쓴다'는 동작으로 이해해야 하며,
        drain() 메소드와 함께 사용해야 한다.
    drain()
        스트림에 기록하는 것이 가능해 질 때까지 기달린다.
        write() 메소드가 코루틴이 아닌 blocking callable임에 유의해야 한다.  이 메소드는
        쓰기버퍼퍼가 차올라 여유가 없으면 대기하여 동일 코루틴이 버퍼를 손상시키는 것을 막는다.
    writeline(data)
        라이트의 리스트를 기록한다.  역시 버퍼에만 쓰므로 drain()을 함께 사용해야 한다.
    close()
        스트림을 닫는다.  스트림을 닫으면 그 하부 소켓도 함께 함께 닫힌다.
        소켓이 닫힐때 시간이 걸릴 수 있기 때문에 wait_closed()와 함께 사용해야 한다.
    can_write_eof()
        하부 트랜스포트 구조가 write_eof() 메소드를 지원하는지 확인한다.
    write_eof()
        쓰기 스트림에 EOF를 삽입한다.
    transport
        하부 비동기 트랜스포트를 리턴한다.
    get_extra_info(name, default=None)
        트랜스 포트 정보를 조사한다.
    wait_closed()
        close()를 호출한 후 스트림이 완전히 닫힐 때까지 기다린다.
"""
import asyncio
from random import random

_port = 7770


''' 클라이언트측 함수 '''


async def run_client(host: str, port: int):
    """ 서버와의 연결을 생성한다. """
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.open_connection(host, port)
    """ show connection info """
    print("[C] connected")
    """ 루프를 돌면서 입력받은 내용을 서버로 보내고, 응답을 받으면 출력한다. """
    while True:
        line = input("[C] enter message: ")
        if not line:
            break
        """ 입력받은 내용을 서버로 전송 """
        payload = line.encode()
        writer.write(payload)
        await writer.drain()
        print(f"[C] sent: {len(payload)} bytes.\n")
        """ 서버로 받은 응답메시지 표시"""
        data = await reader.read(1024)  # type: bytes
        print(f"[C] received: {len(data)} bytes")
        print(f"[C] message: {data.decode()}")
    """ 연결을 종료하나다. """
    print("[C] closing connection...")
    writer.close()
    await writer.wait_closed()


"""
서버측 함수
"""


async def run_server():
    """ 서버를 생성하고 실행 """
    server = await asyncio.start_server(handler, host="127.0.0.1", port=_port)
    async with server:
        """ server_forever()를 호출해야 클라이언트와 연결을 수락한다. """
        await server.serve_forever()


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamReader):
    while True:
        """ 클라이언트가 보내 내용을 받기 """
        data: bytes = await reader.read(1024)
        """ 받은 내용을 출력하고, 가공한 내용을 다시 보내기 """
        peername = writer.get_extra_info('peername')
        print(f"[S] received: {len(data)} bytes from {peername}")
        msg = data.decode()
        print(f"[S] message: {msg}")
        res = msg.upper()[::-1]
        await asyncio.sleep(random() * 2)
        writer.write(res.encode())
        await writer.drain()


async def start():
    await asyncio.wait([run_server(), run_client("127.0.0.1", _port)])


if __name__ == "__main__":
    asyncio.run(start())