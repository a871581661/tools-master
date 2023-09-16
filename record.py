import os
import subprocess
from signal import CTRL_C_EVENT,CTRL_BREAK_EVENT
from subprocess import PIPE, Popen,TimeoutExpired
from configs import recorder_num, is_Master, dir_path


def get_com(file_name: str):
    com_list = []
    for i in range(recorder_num):
        path = os.path.join(dir_path, file_name)
        device_prop = 'Master' if is_Master else 'Subordinate'
        com = f'k4arecorder --device {i}  --color-mode 1080p   --depth-mode  NFOV_2X2BINNED  --rate 30  --imu OFF {device_prop}  {path}.mkv'
        com_list.append(com)
    return com_list[0]


def check_right(proc_list:list):
    for proc in proc_list:
        stderr = proc.stderr.read()
        if stderr:
            raise NameError(stderr.decode('GBK'))
    return True


def start_record(file_name: str):
    com = get_com(file_name)

    proc = Popen(
        com,  # cmd特定的查询空间的命令
        stdin=None,  # 标准输入 键盘
        stdout=PIPE,  # -1 标准输出（演示器、终端) 保存到管道中以便进行操作
        stderr=PIPE,  # 标准错误，保存到管道
        shell=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )

    # check_right(proc_list)
    # pid_list = [proc.pid for proc in proc_list]
    return proc

def end_record(proc:Popen):
    os.kill(proc.pid,CTRL_BREAK_EVENT)
    try:
        outs,errs = proc.communicate(timeout=10)
    except TimeoutExpired:
        proc.kill()
        return False
    return outs,errs

def check_record_file(file_name:str):
    path = os.path.join(dir_path, file_name)
    path = f'{path}.mkv'
    isExist = os.path.exists(path)
    if isExist:
        fsize = os.path.getsize(path)/1024/1024
        return isExist,f'{fsize} M'
    return False,None