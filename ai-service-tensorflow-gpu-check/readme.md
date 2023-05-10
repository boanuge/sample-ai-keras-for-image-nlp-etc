## tensorflow-gpu 동작 확인
코드 실행을 통해 GPU 정상 동작 확인
$ chmod 777 check_run
$ ./check_run

## Monitor GPU-Util usage(%)
$ watch -d -n 0.2 nvidia-smi

## 필요 라이브러리
pip install matplotlib pandas
