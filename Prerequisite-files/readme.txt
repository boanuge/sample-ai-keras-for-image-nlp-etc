[SSH 접속]
우선 VPN 실행이 필요함: Pritunl 실행 --> Authy Desktop (6자리 OTP 번호) --> Pritunl 입력
PuTTY Private Key File 파일 생성 (최초 한번만 하면됨): sub-key.pem --> sub-key.ppk
PuTTY (64-bit)로 터미널 접속
PuTTY Configuration --> Category --> Connection --> SSH --> Auth --> Credentials --> Private key file for authentication: Browse(sub-key.ppk)

[FTP 접속]
- install : sudo apt-get install vsftpd
- config : sudo nano /etc/vsftpd.conf

#vsftpd.conf
pasv_enable=YES
pasv_min_port=1024
pasv_max_port=1048
#chroot_local_user=YES

#write_enable=YES
write_enable=YES

- Start : sudo service vsftpd start

sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo systemctl restart vsftpd
sudo systemctl enable vsftpd

[FileZilla Client로 FTP(파일 전송 프로토콜) 접속]
전송 설정 --> 전송 모드 --> 기본
문자셋 --> UTF-8로 강제 설정
