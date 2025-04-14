# import subprocess
# import threading
#
# def run_command():
#     # 执行命令
#     process = subprocess.Popen(
#         ['python', '-m', 'http.server', '8888'],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
#         bufsize=1,
#         universal_newlines=True
#     )
#     return process
#
# def save_output_to_file(process, file_name):
#     with open(file_name, 'w') as file:
#         while True:
#             output = process.stdout.readline()
#             if output == '' and process.poll() is not None:
#                 break
#             if output:
#                 print(output.strip())
#                 file.write(output)
#
# def main():
#     file_name = 'output.txt'
#     process = run_command()
#     threading.Thread(target=save_output_to_file, args=(process, file_name)).start()
#
# if __name__ == "__main__":
#     main()

import subprocess
import threading
import time

# 使用事件来控制线程的停止
stop_event = threading.Event()

def run_command():
    # 执行命令
    process = subprocess.Popen(
        ['python', '-m', 'http.server', '8888'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    return process

def save_output_to_file(process, file_name):
    with open(file_name, 'w') as file:
        while not stop_event.is_set():
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                file.write(output)
        print("Stopped listening.")

def main():
    file_name = 'output.txt'
    process = run_command()
    threading.Thread(target=save_output_to_file, args=(process, file_name)).start()

    # 等待一段时间或根据需要进行其他操作
    time.sleep(10)  # 例如，等待10秒

    # 设置事件，停止监听
    stop_event.set()

    # 等待进程结束
    process.wait()

    print("Process finished.")

if __name__ == "__main__":
    main()