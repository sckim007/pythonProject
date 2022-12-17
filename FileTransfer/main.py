"""
라이브러리 설치
    pip install paramiko
    pip install scp

SSHManager 클래스
    SSH연결 및 종료, scp 전송 및 다운로드 등의 기능을 포함한 SSHManager 클래스 생성.
"""
import paramiko
from scp import SCPClient, SCPException

class SSHManager:
    def __init__(self):
        self.ssh_client = None

    def create_ssh_client(self, hostname, username, password):
        """ Create SSH client session to remote server """
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password)
        else:
            print("SSH client session exist.")

    def close_ssh_client(self):
        """ Close ssh client session """
        self.ssh_client.close()

    def send_file(self, local_path, remote_path):
        """ Send a single file from to remote path """
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path, preserve_times=True)
        except SCPException:
            raise SCPException.message

    def get_file(self, remote_path, local_path):
        """ Get a single file from remote path """
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)
        except SCPException:
            raise SCPException.message

    def send_command(self, command):
        """ Send a single command """
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ssh_manager = SSHManager()

    """ SSH 연결 설정"""
    ssh_manager.create_ssh_client("192.168.64.149", "sckim007", "rlatjscjf!1")

    """ ssh 명령어 원격 실행 """
    print('-' * 80)
    lines = ssh_manager.send_command("ls -lt /etc/")
    for line in lines:
        print(line, end='')

    """ scp로 파일 업로드 """
    print('-' * 80)
    ssh_manager.send_file("data.txt", "data.txt")

    """ scp로 파일 다운로드 """
    print('-' * 80)
    ssh_manager.get_file("data_server.txt", "data_server.txt")

    """ scp 경로 이동 테스트 """
    ssh_manager.send_command("cd /usr")
    result = ssh_manager.send_command("pwd")
    print(result)
    ssh_manager.send_command("cd local")
    result = ssh_manager.send_command("pwd")
    print(result)

    """ SSH 연결 종료 """
    ssh_manager.close_ssh_client()
