@ 업데이트 @ 2023-12-11

================================================================================
[AI 서버로 FTP 접속] Protocol: SFTP - SSH File Transfer Protocol 사용
================================================================================

install : sudo apt-get install vsftpd

config : sudo nano /etc/vsftpd.conf

# 파일 마지막 줄 아래 붙여 넣을것
#vsftpd.conf
pasv_enable=YES
pasv_min_port=1024
pasv_max_port=1048
write_enable=YES
allow_writeable_chroot=YES
allow_root=YES
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

================================================================================
[Installing Anaconda]
================================================================================

The best way to install Anaconda is to download the latest Anaconda installer bash script, verify it, and then run it.
Find the latest version of Anaconda for Python 3 at the Anaconda Downloads page. At the time of writing, the latest version is 2021.11.
Next, change to the /tmp directory on your server. This is a good directory to download ephemeral items, like the Anaconda bash script.

root@d48f2e696170:/# cd /tmp

Use curl to download the link that you copied from the Anaconda website. You’ll output this to a file called anaconda.sh for quicker use.

root@d48f2e696170:/# sudo apt update
root@d48f2e696170:/# sudo apt install curl

root@d48f2e696170:/# curl https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh --output anaconda.sh

You can now verify the data integrity of the installer with cryptographic hash verification through the SHA-256 checksum. You’ll use the sha256sum command along with the filename of the script:

root@d48f2e696170:/# sha256sum anaconda.sh

You’ll receive output that looks similar to this:

Output
fedf9e340039557f7b5e8a8a86affa9d299f5e9820144bd7b92ae9f7ee08ac60  anaconda.sh

You should check the output against the hashes available at the Anaconda with Python 3 on 64-bit Linux page for your appropriate Anaconda version. As long as your output matches the hash displayed in the sha256 row, you’re good to go.

Now you can run the script:

root@d48f2e696170:/# bash anaconda.sh

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

================================================================================
[jupyter-notebook]
================================================================================

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

================================================================================
[reboot 후 서비스 자동실행]
================================================================================

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

================================================================================
[서버 파일들 백업 @ 루트 디렉토리] @ ai_@_wwhss_alpha_version (3.7G) 설치후
================================================================================

$ sudo tar czvf /path/to/backup_2023-12-11.tar.gz --directory=/ --exclude=proc --exclude=sys --exclude=dev/pts

$ df -Th
Filesystem                  Type      Size  Used Avail Use% Mounted on
udev                        devtmpfs  470M     0  470M   0% /dev
tmpfs                       tmpfs      98M  612K   98M   1% /run
/dev/mapper/ubuntu--vg-root ext4       26G   18G  6.4G  74% /
tmpfs                       tmpfs     489M     0  489M   0% /dev/shm
tmpfs                       tmpfs     5.0M     0  5.0M   0% /run/lock
tmpfs                       tmpfs     489M     0  489M   0% /sys/fs/cgroup
/dev/vda1                   ext2      470M  191M  255M  43% /boot
tmpfs                       tmpfs      98M     0   98M   0% /run/user/0

$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 20.04 LTS
Release:        20.04
Codename:       focal

$ lscpu
Architecture:                    x86_64
CPU op-mode(s):                  32-bit, 64-bit
Byte Order:                      Little Endian
Address sizes:                   39 bits physical, 48 bits virtual
CPU(s):                          4
On-line CPU(s) list:             0-3
Thread(s) per core:              1
Core(s) per socket:              1
Socket(s):                       4
NUMA node(s):                    1
Vendor ID:                       GenuineIntel
CPU family:                      6
Model:                           13
Model name:                      QEMU Virtual CPU version (cpu64-rhel6)
Stepping:                        3
CPU MHz:                         3503.986
BogoMIPS:                        7007.97
Hypervisor vendor:               KVM
Virtualization type:             full
L1d cache:                       128 KiB
L1i cache:                       128 KiB
L2 cache:                        16 MiB
NUMA node0 CPU(s):               0-3
Vulnerability Itlb multihit:     KVM: Vulnerable
Vulnerability L1tf:              Mitigation; PTE Inversion
Vulnerability Mds:               Vulnerable: Clear CPU buffers attempted, no microcode; SMT Host state unknown
Vulnerability Meltdown:          Mitigation; PTI
Vulnerability Mmio stale data:   Not affected
Vulnerability Spec store bypass: Vulnerable
Vulnerability Spectre v1:        Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:        Mitigation; Retpolines, STIBP disabled, RSB filling, PBRSB-eIBRS Not affected
Vulnerability Srbds:             Not affected
Vulnerability Tsx async abort:   Not affected
Flags:                           fpu de pse tsc msr pae mce cx8 apic mtrr pge mca cmov pse36 clflush mmx fxsr sse sse2 syscall nx lm rep_good nopl cpuid tsc_known_freq pni cx16 hypervisor la
                                 hf_lm abm pti
$ free -h
              total        used        free      shared  buff/cache   available
Mem:          976Mi        58Mi       379Mi       1.0Mi       538Mi       752Mi
Swap:         3.7Gi        40Mi       3.7Gi
