## tensorflow-gpu 동작 확인
코드 실행을 통해 GPU 정상 동작 확인
$ chmod 777 check_run
$ ./check_run

## Monitor GPU-Util usage(%)
$ watch -d -n 0.2 nvidia-smi

## 필요 라이브러리
pip install matplotlib pandas

## GPU에 할당(사용)되는 메모리 크기 제한
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
gpu_memory_limit=1024*10 # only allocate 10GB of memory on the gpus[0], i.e. first GPU
if gpus:
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=gpu_memory_limit)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print("GPU memory allocation(",gpu_memory_limit,")",
          "# of Physical GPU(",len(gpus),") # of Logical GPU(",len(logical_gpus),")")
  except RuntimeError as e:
    print(e) # Virtual devices must be set before GPUs have been initialized
