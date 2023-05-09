[AI 서버 오토스케일링 정책]
Route53(도메인생성) --> ALB(로드밸런서/리스너추가) --> TG(타겟그룹/포워딩추가)
--> AMI(이미지생성) --> LT(런치템플릿/이미지추가) --> ASG(오토스케일링정책)
240(60x4)개 요청(1분기준)시 : ALB에서 EC2 인스턴스 추가
Desired/Minimum capacity : 2
Maximum capacity : 8

EC2-AI-GPU
Instance Size	GPU	vCPUs	Memory	Instance Storage	On-Demand Price/hr*
g4dn.2xlarge	1	8	32	1 x 225 NVMe SSD	$0.752
g4dn.2xlarge @ ap-northeast-2a
OS : Ubuntu 22.04 x86_64
RAM : 32G
GPU : NVIDIA GPU x1개 + CPU x8개
DISK : 64G (SSD)

Network settings --> VPC : 10.254.0.0/16, 10.255.0.0/16
Network settings --> Subnet : 10.255.120.0/24
Network settings --> Auto-assign public IP : Disable
Network settings --> Existing Security Group : SG-EC2-AI-GPU
Advanced details --> User data - optional
#cloud-config
system_info:
  default_user:
    name: metaverse

[Security Groups]
SG-EC2-AI-GPU

IP version, Type, Protocol, Port range, Source, Description
22	TCP	10.0.0.22/32	SG-EC2-AI-GPU 	live-vpn @ metaverse
1024 - 1048	TCP	0.0.0.0/0	SG-EC2-AI-GPU 	ftp passive mode @ metaverse
5000 - 5009	TCP	0.0.0.0/0	SG-EC2-AI-GPU 	python flask @ ai-service (live)
5550 - 5559	TCP	0.0.0.0/0	SG-EC2-AI-GPU 	python flask @ ai-service (test)
9999	TCP	0.0.0.0/0	SG-EC2-AI-GPU 	jupyter notebook @ metaverse
20 - 21	TCP	0.0.0.0/0	SG-EC2-AI-GPU 	FileZilla Client @ metaverse

사용자명 (metaverse//비번)
sudo passwd root
sudo passwd metaverse

[NVIDIA GPU]
#CUDA 설치
$ sudo lshw -c display
  *-display:1 UNCLAIMED
       description: 3D controller
       product: TU104GL [Tesla T4]
       vendor: NVIDIA Corporation
       physical id: 1e
       bus info: pci@0000:00:1e.0
       version: a1
       width: 64 bits
       clock: 33MHz
       capabilities: pm pciexpress msix cap_list
       configuration: latency=0
       resources: iomemory:80-7f iomemory:80-7f memory:fd000000-fdffffff memory:840000000-84fffffff memory:850000000-851ffffff
$ lspci | grep -i nvidia
00:1e.0 3D controller: NVIDIA Corporation TU104GL [Tesla T4] (rev a1)

$ sudo dpkg --add-architecture i386
$ sudo apt-get update
$ sudo apt-get install libnvidia-compute-495:i386 libnvidia-decode-495:i386 \
 libnvidia-encode-495:i386 libnvidia-extra-495:i386 libnvidia-fbc1-495:i386 \
 libnvidia-gl-495:i386
$ sudo reboot

$ cd /tmp
$ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
$ sudo dpkg -i cuda-keyring_1.0-1_all.deb
$ sudo apt-get update
$ sudo apt-get install cuda
$ sudo apt-get install nvidia-gds
$ sudo apt-get install libcudnn8
$ sudo apt-get install libcudnn8-dev
$ sudo reboot

#CUDA 환경변수 등록
$ nano ~/.bashrc
# 파일 제일 윗 부분에 붙여 넣을것
export CUDA_HOME=/usr/local/cuda-12.1
export PATH=/usr/local/cuda-12.1/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH
# 끝.
$ source ~/.bashrc



[AI 서버로 FTP 접속]

install : sudo apt-get install vsftpd

config : sudo nano /etc/vsftpd.conf

# 파일 마지막 줄 아래 붙여 넣을것
#vsftpd.conf
pasv_enable=YES
pasv_min_port=1024
pasv_max_port=1048
#chroot_local_user=YES

#write_enable=YES
write_enable=YES
# 끝.

run below commands :
sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo systemctl restart vsftpd
sudo systemctl enable vsftpd
sudo service vsftpd start

EC2 inbound : 1024 ~ 1048 , 21 , 20

FileZilla Client로 FTP(파일 전송 프로토콜) 접속

전송 설정 --> 전송 모드 --> 기본

문자셋 --> UTF-8로 강제 설정



[Installing Anaconda]

The best way to install Anaconda is to download the latest Anaconda installer bash script, verify it, and then run it.
Find the latest version of Anaconda for Python 3 at the Anaconda Downloads page. At the time of writing, the latest version is 2021.11.
Next, change to the /tmp directory on your server. This is a good directory to download ephemeral items, like the Anaconda bash script.

(base) root@d48f2e696170:/# cd /tmp

Use curl to download the link that you copied from the Anaconda website. You’ll output this to a file called anaconda.sh for quicker use.

(base) root@d48f2e696170:/# curl https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh --output anaconda.sh

You can now verify the data integrity of the installer with cryptographic hash verification through the SHA-256 checksum. You’ll use the sha256sum command along with the filename of the script:

(base) root@d48f2e696170:/# sha256sum anaconda.sh

You’ll receive output that looks similar to this:

Output
fedf9e340039557f7b5e8a8a86affa9d299f5e9820144bd7b92ae9f7ee08ac60  anaconda.sh

You should check the output against the hashes available at the Anaconda with Python 3 on 64-bit Linux page for your appropriate Anaconda version. As long as your output matches the hash displayed in the sha256 row, you’re good to go.

Now you can run the script:

(base) root@d48f2e696170:/# bash anaconda.sh

You’ll receive the following output:

Output
Welcome to Anaconda3 2021.11

In order to continue the installation process, please review the license agreement.
Please, press ENTER to continue (press Space)
>>>  
Press ENTER to continue and then press ENTER to read through the license. Once you’re done reading the license, you’ll be prompted to approve the license terms:

Output
Do you approve the license terms? [yes|no]
As long as you agree, type yes.

At this point, you’ll be prompted to choose the location of the installation. You can press ENTER to accept the default location, or specify a different location to modify it.

Output
Anaconda3 will now be installed into this location:
/home/sammy/anaconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/home/sammy/anaconda3] >>>

The installation process will continue. Note that it may take some time.

Once installation is complete, you’ll receive the following output:

Output
...
installation finished.
Do you wish the installer to initialize Anaconda3
by running conda init? [yes|no]
[no] >>>
Type yes so that you can initialize Anaconda3.

Output
...
Thank you for installing Anaconda3!
...
You can now activate the installation by sourcing the ~/.bashrc file:

(base) root@d48f2e696170:/# source ~/.bashrc



[jupyter-notebook]

(base) root@d48f2e696170:/# jupyter notebook --generate-config
Writing default config to: /root/.jupyter/jupyter_notebook_config.py

(base) root@d48f2e696170:/# nano ~/.jupyter/jupyter_notebook_config.py
# 파일 업데이트
## The IP address the notebook server will listen on.
#  Default: 'localhost'
# c.NotebookApp.ip = 'localhost'
c.NotebookApp.ip = '*'

## The directory to use for notebooks and kernels.
#  Default: ''
c.NotebookApp.notebook_dir = '/root/AI'

c.NotebookApp.open_browser = False

## The port the notebook server will listen on (env: JUPYTER_PORT).
#  Default: 8888
c.NotebookApp.port = 9999
# 끝.

(base) root@d48f2e696170:/# ipython
Python 3.8.8 (default, Apr 13 2021, 19:58:26)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from notebook.auth import security

In [2]: security.passwd()
Enter password:
Verify password:
Out[2]: 'argon2:$argon2id$v=19$m=10240,t=10,p=8$VyDYOAVzhQRqfI1vOo+DdA$DzqDzhTwDszdIaAwqLv4gg'

In [3]: exit

(base) root@d48f2e696170:/# jupyter notebook

    To access the notebook, open this file in a browser:
        file:///home/metaverse/.local/share/jupyter/runtime/nbserver-5486-open.html
    Or copy and paste one of these URLs:
        http://192.168.31.50:9999/?token=5b9866c38a202217304e697b89b5533518d8677606562b27
     or http://127.0.0.1:9999/?token=5b9866c38a202217304e697b89b5533518d8677606562b27

(base) root@d48f2e696170:/# nano jupyter_notebook

nohup jupyter notebook --allow-root > error.log &

(base) root@d48f2e696170:/# chmod 777 jupyter_notebook
(base) root@d48f2e696170:/# ./jupyter_notebook

ps -ef | grep jupyter



[requirements.txt]
flask==1.1.2
waitress==2.1.2
keras==2.10.0
tensorflow==2.10.0
transformers==4.8.0
numpy==1.23
pandas==1.3.4
matplotlib==3.4.3
pillow==8.4.0

(base) root@d48f2e696170:/# pip install -r requirements.txt
# $ export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
# or Setting the environment variable in a script: 
# import os
# os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'



[reboot 후 서비스 자동실행]

(base) root@d48f2e696170:/# sudo nano /etc/rc.local

# 파일 내용
#!/bin/bash

cd "/home/metaverse/ai-service-image @ 2023-05-01/"
nohup /home/metaverse/anaconda3/bin/python flask_ai_service_image.py > error.log &

cd "/home/metaverse/AI-Image-Classification @ 2023-05-01/"
nohup /home/metaverse/anaconda3/bin/python flask_Image_Classification.py > error.log &

exit 0
# 끝.

(base) root@d48f2e696170:/# sudo chmod +x /etc/rc.local

(base) root@d48f2e696170:/# sudo nano /lib/systemd/system/rc-local.service

# 파일 마지막 줄 아래 붙여 넣을것
[Install]
WantedBy=multi-user.target
# 끝.

(base) root@d48f2e696170:/# sudo systemctl enable rc-local.service
(base) root@d48f2e696170:/# sudo systemctl start rc-local.service
(base) root@d48f2e696170:/# sudo systemctl status rc-local.service
● rc-local.service - /etc/rc.local Compatibility
     Loaded: loaded (/lib/systemd/system/rc-local.service; enabled; vendor preset: enabled)
    Drop-In: /usr/lib/systemd/system/rc-local.service.d
             └─debian.conf
     Active: active (running) since Thu 2023-05-04 04:44:11 UTC; 24s ago
       Docs: man:systemd-rc-local-generator(8)
    Process: 531 ExecStart=/etc/rc.local start (code=exited, status=0/SUCCESS)
      Tasks: 74 (limit: 37950)
     Memory: 2.9G
        CPU: 23.617s
     CGroup: /system.slice/rc-local.service
             ├─540 /home/metaverse/anaconda3/bin/python flask_ai_service_image.py
             └─541 /home/metaverse/anaconda3/bin/python flask_Image_Classification.py

(base) root@d48f2e696170:/#
