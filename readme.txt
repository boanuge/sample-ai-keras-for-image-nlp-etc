@ 업데이트 @ 2023-12-11

================================================================================
[ 서버정보 및 FTP 접속 ] Protocol: SFTP - SSH File Transfer Protocol 사용
================================================================================

$ free -h
              total        used        free      shared  buff/cache   available
Mem:          976Mi       115Mi       708Mi       2.0Mi       151Mi       718Mi
Swap:         3.7Gi          0B       3.7Gi

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

$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 20.04 LTS
Release:        20.04
Codename:       focal

================================================================================
[ 웹서버 설치 @ /var/www/html ] @ Apache2 + PHP7.4 및 Node.js
================================================================================

아파치 웹 서버 설치:
$ sudo apt update
$ sudo apt install apache2

PHP 설치:
$ sudo apt install -y php7.4
$ sudo apt install -y libapache2-mod-php7.4

$ php -v
PHP 7.4.3-4ubuntu2.19 (cli) (built: Jun 27 2023 15:49:59) ( NTS )
Copyright (c) The PHP Group
Zend Engine v3.4.0, Copyright (c) Zend Technologies
    with Zend OPcache v7.4.3-4ubuntu2.19, Copyright (c), by Zend Technologies

$ sudo nano /etc/php/7.4/apache2/php.ini
;short_open_tag = Off
short_open_tag = On
; register_globals 옵션은 PHP 5.3.0에서 DEPRECATED 되었고,
; PHP 5.4.0 부터는 제거되어서 사용할 수 없다.
;register_globals = On

아파치 모듈 활성화:
$ sudo a2enmod php7.4
Considering dependency mpm_prefork for php7.4:
Considering conflict mpm_event for mpm_prefork:
Considering conflict mpm_worker for mpm_prefork:
Module mpm_prefork already enabled
Considering conflict php5 for php7.4:
Module php7.4 already enabled

로그 파일 비활성화:
가장 간단한 방법은 아파치 웹 서버에서 로그를 비활성화하는 것입니다.
아파치 설정 파일에서 ErrorLog 및 CustomLog 를 주석 처리 합니다.
$ sudo nano /etc/apache2/apache2.conf
#LogLevel warn
LogLevel error
ErrorLog ${APACHE_LOG_DIR}/error.log
AddType application/x-httpd-php .php .htm .html .inc
AddType application/x-httpd-php-source .phps

아파치 서비스 재시작:
$ sudo systemctl restart apache2

서비스 부팅시 재시작 등록:
$ sudo systemctl enable apache2

서비스 상태 확인:
$ sudo systemctl status apache2

Node.js 14.21.3 버전 및 Node Package Manager 6.14.18 버전 설치:
$ curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
$ sudo apt install nodejs
$ cd /root/chat_@_node.js
$ npm install

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
cd /root/chat_@_node.js
nohup /usr/bin/node server.js > chat_log.txt 2>&1 &
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
    Drop-In: /lib/systemd/system/rc-local.service.d
             └─debian.conf
     Active: active (running) since Mon 2023-12-11 19:17:41 KST; 5s ago
       Docs: man:systemd-rc-local-generator(8)
    Process: 16634 ExecStart=/etc/rc.local start (code=exited, status=0/SUCCESS)
      Tasks: 11 (limit: 1126)
     Memory: 24.2M
     CGroup: /system.slice/rc-local.service
             └─16635 /usr/bin/node server.js

Dec 11 19:17:41 integritian.cafe24.com systemd[1]: Starting /etc/rc.local Compatibility...
Dec 11 19:17:41 integritian.cafe24.com systemd[1]: Started /etc/rc.local Compatibility.

(base) root@d48f2e696170:/# ps -ef | grep node
root       16436    2585  0 19:11 pts/0    00:00:00 /usr/bin/node server.js
root       16545    2585  0 19:13 pts/0    00:00:00 grep --color=auto node
(base) root@d48f2e696170:/# sudo kill -9 16436
(base) root@d48f2e696170:/# ps -ef | grep node
root       16557    2585  0 19:13 pts/0    00:00:00 grep --color=auto node
[1]+  Killed                  nohup /usr/bin/node server.js > chat_log.txt 2>&1
(base) root@d48f2e696170:/#
