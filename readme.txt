@ 업데이트 @ 2023-12-11

================================================================================
[ 서버정보 및 FTP 접속 ] Protocol: SFTP - SSH File Transfer Protocol 사용
================================================================================

$ df -Th
Filesystem                  Type      Size  Used Avail Use% Mounted on
udev                        devtmpfs  470M     0  470M   0% /dev
tmpfs                       tmpfs      98M  628K   98M   1% /run
/dev/mapper/ubuntu--vg-root ext4       26G  2.8G   22G  12% /
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
Flags:                           fpu de pse tsc msr pae mce cx8 apic mtrr pge mca cmov pse36 clflush mmx fxsr sse sse2 syscall nx l
                                 m rep_good nopl cpuid tsc_known_freq pni cx16 hypervisor lahf_lm abm pti

$ free -h
              total        used        free      shared  buff/cache   available
Mem:          976Mi       115Mi       708Mi       2.0Mi       151Mi       718Mi
Swap:         3.7Gi          0B       3.7Gi

================================================================================
[ 서버파일 백업 @ 루트 디렉토리 ]
================================================================================

$ sudo tar czvf /path/to/backup_2023-12-11.tar.gz --directory=/ --exclude=proc --exclude=sys --exclude=dev/pts

================================================================================
[ 웹서버 설치 @ /var/www/html ] @ Nginx + PHP 및 Node.js
================================================================================

Nginx 설치:
$ sudo apt update
$ sudo apt install nginx

Nginx 서비스 시작:
$ sudo systemctl start nginx

Nginx 부팅 시 자동 실행 설정:
$ sudo systemctl enable nginx

PHP-FPM 설치:
PHP를 Nginx와 통합하기 위해 PHP-FPM (FastCGI Process Manager) 및 php 모듈들 설치
$ sudo apt install php7.4-fpm php7.4-common

(base) $ sudo nano /etc/nginx/sites-available/default
# PHP 사용을 위해 아래 부분 코멘트 # 제거 및 추가
        # pass PHP scripts to FastCGI server
        location ~ \.php$ {
                include snippets/fastcgi-php.conf;
                # With php-fpm (or other unix sockets):
                fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;
                # With php-cgi (or other tcp sockets):
                #fastcgi_pass 127.0.0.1:9000;
        }
# 끝.

Node.js 설치:
Node.js를 설치하기 위해서는 Node.js의 패키지 매니저인 NPM(Node Package Manager)도 함께 설치
$ sudo apt install nodejs npm

================================================================================
[ Installing Anaconda ]
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

일반적으로 Anaconda를 설치할 때 /tmp 폴더에 일시적으로 설치 파일이나 데이터가 저장됩니다.
Anaconda 설치가 완료된 후에는 해당 폴더를 삭제해도 됩니다.
$ sudo rm -rf /tmp/*

================================================================================
[ reboot 후 서비스 자동실행 ]
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
