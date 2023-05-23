[AI 서버 오토스케일링 정책]
Route53 : live.ai-api.com (도메인생성)
--> ALB : LIVE-ALB-AI-API (로드밸런서/리스너추가)
--> TG : LIVE-TG-AI-API-5001 ~ LIVE-TG-AI-API-5009 (타겟그룹/포워딩추가)
--> AMI : LIVE-AMI-AI-API-V1 ~ LIVE-AMI-AI-API-V9 (이미지생성)
--> LT : LIVE-LT-AI-API (런치템플릿/새버전생성/이미지변경)
--> ASG : LIVE-ASG-AI-API (오토스케일링정책/인스턴스새로고침)
1분 내 200개 요청시 : EC2 추가 생성 오토스케일링그룹 내 자동크기조정에서 변경 가능
- 요청 타임아웃 10초일 때 이미지모델 추론서버 하나당 1분 내 약 100개 정도 핸들링
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

[NVIDIA GPU to use CUDA]

# Remove existing nvidia drivers if any

$ sudo apt-get purge nvidia*
$ sudo apt-get autoremove
$ sudo apt-get autoclean
$ sudo rm -rf /usr/local/cuda*

# Update installing packages

$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install build-essential

# Install the nvidia driver

$ sudo apt install nvidia-driver-525
$ sudo apt-get install dkms nvidia-modprobe
$ sudo reboot
$ watch -d -n 0.2 nvidia-smi

# CUDA Toolkit 11.7 Update 1 Downloads
https://developer.nvidia.com/cuda-11-7-1-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local

$ cd /tmp
$ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
$ sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
$ wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda-repo-ubuntu2204-11-7-local_11.7.1-515.65.01-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu2204-11-7-local_11.7.1-515.65.01-1_amd64.deb
$ sudo cp /var/cuda-repo-ubuntu2204-11-7-local/cuda-*-keyring.gpg /usr/share/keyrings/
$ sudo apt-get update
$ sudo apt-get -y install cuda
$ sudo reboot

# 추가 작업 (다운그레이드) 12.1 --> 11.7

$ sudo apt update && rm -rf /var/lib/apt/lists/*
$ sudo add-apt-repository multiverse
$ sudo apt update
$ sudo dpkg --add-architecture i386
$ sudo apt-get install libnvidia-compute-495:i386 libnvidia-decode-495:i386 \
 libnvidia-encode-495:i386 libnvidia-extra-495:i386 libnvidia-fbc1-495:i386 \
 libnvidia-gl-495:i386
$ sudo apt install nvidia-cuda-toolkit
$ sudo apt-get install nvidia-gds
$ sudo apt-get install cuda-11.7
$ sudo reboot

# 환경 패스 설정
$ nano ~/.bashrc
# 파일 제일 위쪽에 붙여 넣을것
export PATH=/usr/local/cuda-11.7/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
# 끝.
$ source ~/.bashrc

# Download cuDNN v8.7.0 (November 28th, 2022) for CUDA 11.x
https://developer.nvidia.com/downloads/c118-cudnn-linux-8664-87084cuda11-archivetarz
cudnn-linux-x86_64-8.7.0.84_cuda11-archive.tar.xz <-- 865,648KB file size

$ cd /tmp
$ tar -xvf cudnn-linux-x86_64-8.7.0.84_cuda11-archive.tar.xz
$ sudo cp cudnn-linux-x86_64-8.7.0.84_cuda11-archive/include/cudnn* /usr/local/cuda/include
$ sudo cp cudnn-linux-x86_64-8.7.0.84_cuda11-archive/lib/libcudnn* /usr/local/cuda/lib64
$ sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
$ sudo ln -sf /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_adv_train.so.8.4.1 /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_adv_train.so.8
$ sudo ln -sf /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_ops_infer.so.8.4.1  /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_ops_infer.so.8
$ sudo ln -sf /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_cnn_train.so.8.4.1  /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_cnn_train.so.8
$ sudo ln -sf /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_adv_infer.so.8.4.1  /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_adv_infer.so.8
$ sudo ln -sf /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_ops_train.so.8.4.1  /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_ops_train.so.8
$ sudo ln -sf /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_cnn_infer.so.8.4.1 /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn_cnn_infer.so.8
$ sudo ln -sf /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn.so.8.4.1 /usr/local/cuda-11.7/targets/x86_64-linux/lib/libcudnn.so.8
$ sudo reboot

# Monitor GPU-Util usage(%)

$ watch -d -n 0.2 nvidia-smi



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

[주피터 노트북 자동실행]

$ sudo nano /etc/systemd/system/jupyter.service
# 파일 내용

[Unit]
Description=Jupyter Notebook
After=network.target

[Service]
Type=simple
User=metaverse
ExecStart=/home/gbike/anaconda3/bin/jupyter notebook --allow-root

[Install]
WantedBy=multi-user.target
# 끝.

$ sudo systemctl enable jupyter.service
$ sudo systemctl start jupyter.service
$ sudo systemctl status jupyter.service
● jupyter.service - Jupyter Notebook
     Loaded: loaded (/etc/systemd/system/jupyter.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2023-05-24 08:25:09 KST; 3min 1s ago
   Main PID: 500 (jupyter-noteboo)
      Tasks: 1 (limit: 18828)
     Memory: 123.1M
        CPU: 1.413s
     CGroup: /system.slice/jupyter.service
             └─500 /home/metaverse/anaconda3/bin/python /home/metaverse/anaconda3/bin/jupyter-notebook --allow-root
