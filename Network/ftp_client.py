"""
Ubuntu 20.04에 ftp 서버를 설치하는 절차.
    1. vsftpd 패키지 설치
    $ sudo apt-get install vsftpd

    2. vsftpd.conf 수정
    $ sudo nano /etc/vsftpd.conf
    ...
    listen=NO
    listen_ipv6=YES
    anonymous_enable=NO
    local_enable=YES
    chroot_local_user=YES
    allow_writeable_chroot=YES
    local_root=/data/ftp/files
    write_enable=YES
    local_umask=022
    dirmessage_enable=YES
    userlist_enable=YES
    userlist_file=/etc/vsftpd.userlist
    userlist_deny=NO

    3. ftp를 위한 사용자를 추가
    $ sudo adduser ftpuser

    4. 설정파일에 사용자 이름을 추가
    $ echo "vsftpd test file" | sudo tee /data/ftp/files/test.txt

    5. ftp에서 업로드한 파일을 저장시 사용할 경로를 생성
    $ sudo mkdir -p /data/ftp
    $ sudo chown nobody:nogroup /data/ftp
    $ sudo chmod a-w /data/ftp

    6. 파일 업로드를 위한 디렉토리를 생성
    $ sudo mkdir /data/ftp/files
    $ sudo chown ftpuser:ftpuser /data/ftp/files

    7. vsftpd 서비스 재시작
    $ sudo systemctl restart vsftpd
"""
import ftplib
import os

class FtpManager:
    def __init__(self):
        self.ftp_client = None

    def create_ftp_client(self, hostname, username, password):
        """ Create FTP client session to remote server """
        try:
            if self.ftp_client is None:
                self.ftp_client = ftplib.FTP()
                self.ftp_client.connect(host=hostname, port=21)
                self.ftp_client.encoding = 'utf-8'
                s = self.ftp_client.login(user=username, passwd=password)

                """ 현재 디렉토리 출력 """
                print('현재디렉토리:', self.ftp_client.pwd())
            else:
                print("FTP client session exist.")
        except Exception as e:
            print(e)

    def close_ftp_client(self):
        """ Close ftp client session """
        self.ftp_client.quit()
        self.ftp_client.close()

    def send_file(self, local_path, remote_path):
        """ Send a single file from to remote path """
        try:
            with open(file=local_path, mode='rb') as wf:
                self.ftp_client.storbinary(f'STOR {remote_path}', wf)
            print(self.ftp_client.dir())
        except Exception as e:
            print(e)

    def send_files(self, local_dir, remote_dir):
        """ Send a multiple file from to remote path """
        try:
            self.ftp_client.cwd(remote_dir)

            list = os.listdir(local_dir)
            print(list)
            for file in list:
                with open(file=r'{}\{}'.format(local_dir, file), mode='rb') as f:
                    self.ftp_client.storbinary('STOR {}'.format(file), f)
            print(self.ftp_client.dir())
        except Exception as e:
            print(e)

    def get_file(self, local_path, remote_path):
        """ Get a single file from remote path """
        try:
            with open(file=local_path, mode='wb') as rf:
                self.ftp_client.retrbinary(f'RETR {remote_path}', rf.write)
        except Exception as e:
            print(e)

    def get_files(self, remote_dir, local_dir):
        """ Get a multiple files from remote path """
        try:
            self.ftp_client.cwd(remote_dir)

            flist = self.ftp_client.nlst()
            print(flist)
            for file in flist:
                file_path = r'{}\{}'.format(local_dir, file)
                with open(file=file_path, mode='wb') as rf:
                    self.ftp_client.retrbinary(f'RETR {file}', rf.write)
        except Exception as e:
            print(e)


    def create_dir(self, dir_name):
        """ Create directory """
        try:
            if self.ftp_client is not None:
                self.ftp_client.mkd(dir_name)
        except Exception as e:
            print(e)

    def remove_dir(self, dir_name):
        """ Remove directory """
        try:
            if self.ftp_client is not None:
                self.ftp_client.rmd(dir_name)
        except Exception as e:
            print(e)

    def change_dir(self, dir_name):
        """ Change directory """
        try:
            if self.ftp_client is not None:
                self.ftp_client.cwd(dir_name)

            """ 현재 디렉토리를 출력 """
            print(self.ftp_client.dir())
        except Exception as e:
            print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ftp_manager = FtpManager()

    """ SSH 연결 설정"""
    ftp_manager.create_ftp_client("192.168.64.149", "ftpuser", "rlatjscjf!1")

    """ 디렉토리 생성 """
    #ftp_manager.create_dir('testdir')

    """ 디렉토리 삭제 """
    #ftp_manager.remove_dir('testdir')

    """ 디렉토리 변경 """
    #ftp_manager.change_dir('testdir')

    """ 하나의 파일 업로드 """
    #print('-' * 80)
    #ftp_manager.send_file("data.txt", "data.txt")

    """ 현재 디렉토리 파일들을 서버의 testdir 디렉토리로 파일 업로드 """
    #print('-' * 80)
    #local_dir = os.getcwd()
    #ftp_manager.send_files(local_dir, "testdir")

    """ ftp로 파일 다운로드 """
    #print('-' * 80)
    #ftp_manager.get_file("data_server.txt", "data_server.txt")

    """ 서버의 testdir 디렉토리의 모든 파일을 files 디렉토리로 다운로드 """
    print('-' * 80)
    local_dir = r"{}\files".format(os.getcwd())
    ftp_manager.get_files('testdir', local_dir)

    """ SSH 연결 종료 """
    ftp_manager.close_ftp_client()
