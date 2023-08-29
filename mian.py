# 导入所需的库
import tkinter as tk
import importlib
import socket
import threading
import os  # 新增: 导入os模块
from cryptography.fernet import Fernet

                        
# 全局变量用于跟踪服务器状态和套接字
server_running = False
server_socket = None  # 添加这个变量来存储服务器套接字
server_stopped = False

# 创建一个加密/解密对象
cipher_suite = None

# 新增: 定义VPN启动和停止函数
def start_vpn():
    # 启动Clash for Windows客户端
    os.system("\"C:\\Users\\Administrator\\AppData\\Local\\Programs\\Clash for Windows\\Clash for Windows.exe\"")
    print("VPN Connection Started")

def stop_vpn():
    # 停止Clash for Windows客户端
    os.system("taskkill /f /im \"Clash for Windows.exe\"")
    print("VPN Connection Stopped")

# 定义处理客户端连接的函数
def handle_client(client_socket):
    # 首先，接收从客户端发送过来的加密密码
    password_data = client_socket.recv(1024)

    # 使用密钥解密密码
    decrypted_password = cipher_suite.decrypt(password_data).decode('utf-8')

    # 验证密码是否正确
    if decrypted_password == "12345678":
        print("Password verified.")

        # 进行数据通讯
        while True:
            # 接收从客户端发送过来的加密数据
            data = client_socket.recv(1024)

            # 解密数据
            decrypted_data = cipher_suite.decrypt(data)
            print(f"Received data: {decrypted_data.decode('utf-8')}")

            # 如果没有数据，则退出循环
            if not data:
                break

            # 对要发送的回复进行加密
            encrypted_reply = cipher_suite.encrypt(b"Hello, client!")

            # 发送加密后的回复
            client_socket.send(encrypted_reply)

        # 关闭客户端连接
        client_socket.close()
    else:
        # 如果密码不正确，则关闭连接
        print("Invalid password. Connection closed.")
        client_socket.close()

# 网络服务器和数据加密模块
def server_and_encryption():
    # 使用全局变量 server_running
    global server_running, cipher_suite

    # 生成一个新的加密密钥
    key = Fernet.generate_key()

    # 创建一个加密/解密对象
    cipher_suite = Fernet(key)

    # 启动服务器
    start_server()

# 定义启动服务器的函数
def start_server():
    global server_socket  # 使用全局变量 server_socket
    # 创建一个新的套接字对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定服务器地址和端口
    server_socket.bind(("0.0.0.0", 9999))

    # 监听连接，最多允许5个等待连接的客户端
    server_socket.listen(5)
    print("Listening for connections...")  # 输出监听状态

    # 使用全局变量 server_running 控制 while 循环
    while server_running:
        # 添加检查条件
        if server_socket is None or server_stopped:
            print("Server socket is None or server is stopped, exiting loop.")
            break

        try:
            # 等待客户端连接
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr} has been established.")  # 输出连接成功的信息
            print(f"Server is running on IP: {addr[0]}, PORT: {addr[1]}")  # 输出服务器实际绑定的IP和端口
        except OSError:
            print("Error during accept(), possibly because socket was closed. Exiting loop.")
            break

        # 在一个新的线程里处理客户端连接
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()  # 启动新的线程

# 网络连接操作模块：启动网络连接
def start_connection():
    global server_running  # 使用全局变量 server_running
    global server_stopped  # 新增全局变量 server_stopped
    server_stopped = False  # 设置为 False 表示服务器正在运行
    start_vpn()  # 新增: 在启动服务器之前启动VPN
    print("VPN Connection Started")  # 输出启动信息
    server_running = True  # 设置服务器状态为运行中

    # 在一个新的线程中运行服务器和加密模块
    server_thread = threading.Thread(target=server_and_encryption)
    server_thread.start()  # 启动线程

    # 根据当前的背景色来切换按钮的颜色
    if connection_button['bg'] == "#43464B":
        connection_button['bg'] = "red"
    else:
        connection_button['bg'] = "#43464B"

# 网络连接操作模块：停止网络连接
def stop_connection():
    global server_running, server_socket  # 使用全局变量 server_running 和 server_socket
    global server_stopped  # 新增全局变量 server_stopped
    server_stopped = True  # 设置为 True 表示服务器已停止
    
    # 断开VPN连接
    stop_vpn()  # 新增: 在停止服务器之后停止VPN
    print("VPN Connection Stopped")  # 输出停止信息
    
    # 停止服务器
    server_running = False  # 设置服务器状态为停止

    # 如果服务器套接字存在，则尝试关闭并重置为 None
    if server_socket:
        try:
            server_socket.close()  # 先关闭套接字
            print("Server socket closed successfully.")
        except Exception as e:
            print(f"Error closing the socket: {e}")
        server_socket = None  # 然后设置为 None

    # 根据当前的背景色来切换按钮的颜色
    if connection_button['bg'] == "#43464B":
        connection_button['bg'] = "red"
    else:
        connection_button['bg'] = "#43464B"

# 菜单模块
def show_menu():
    # 创建一个新的菜单
    menu = tk.Menu(root, tearoff=0)
    # 添加两个选项到菜单
    menu.add_command(label="选项 1")
    menu.add_command(label="选项 2")
    # 在当前鼠标的位置显示菜单
    menu.post(root.winfo_pointerx(), root.winfo_pointery())

# 按钮创建模块
def create_bevel_button(frame, text, command, x, y, w, h, color):
    # 创建一个自定义按钮
    button = tk.Button(frame, text=text, command=command, bg=color, fg='white', padx=w, pady=h)
    button.grid(row=0, column=x)
    return button

# 添加断开连接按钮
def create_buttons():
    global connection_button
    connection_button = create_bevel_button(second_row_frame, "启动连接", start_connection, 2, 0, 20, 5, "#43464B")
    disconnect_button = create_bevel_button(second_row_frame, "断开连接", stop_connection, 3, 0, 20, 5, "#43464B")

# 信号检测模块
def show_signal_detection():
    # 导入和重新加载 chat_wife 模块
    chat_wife = importlib.import_module('chat_wife')
    importlib.reload(chat_wife)
    # 调用 chat_wife 模块中的 show_signal_detection 函数
    chat_wife.show_signal_detection(root)

# GUI初始化和设置模块
root = tk.Tk()
root.title("ADS VPN系统")
root.state('zoomed')
root.configure(bg='black')

# 第一行功能按钮和标签模块
first_row_frame = tk.Frame(root, bg='black')
first_row_frame.pack(pady=10, anchor='w')

# 添加各种功能标签和设置对应的点击事件
logo_label = tk.Label(first_row_frame, text="LOGO", width=10, bg='black', fg='white', cursor="hand2")
logo_label.grid(row=0, column=0)
logo_label.bind("<Button-1>", lambda e: show_menu())

signal_detection_label = tk.Label(first_row_frame, text="信号检测", width=15, bg='black', fg='white', cursor="hand2")
signal_detection_label.grid(row=0, column=1)
signal_detection_label.bind("<Button-1>", lambda e: show_signal_detection())

performance_label = tk.Label(first_row_frame, text="性能参数", width=15, bg='black', fg='white', cursor="hand2")
performance_label.grid(row=0, column=2)
performance_label.bind("<Button-1>", lambda e: show_menu())

encryption_label = tk.Label(first_row_frame, text="高加密模式", width=15, bg='black', fg='white', cursor="hand2")
encryption_label.grid(row=0, column=3)
encryption_label.bind("<Button-1>", lambda e: show_menu())

online_account_label = tk.Label(first_row_frame, text="在线账号", width=15, bg='black', fg='white', cursor="hand2")
online_account_label.grid(row=0, column=4)
online_account_label.bind("<Button-1>", lambda e: show_menu())

# 第二行功能按钮模块
second_row_frame = tk.Frame(root, bg='black')
second_row_frame.pack(pady=10, anchor='w') 
create_buttons()

# 添加登录和连接启动按钮
login_button = create_bevel_button(second_row_frame, "Login", start_connection, 0, 0, 20, 5, "#43464B")
plus_symbol_label = tk.Label(second_row_frame, text="+", fg="blue", font=("Helvetica", 24), bg='black')
plus_symbol_label.grid(row=0, column=1)
connection_button = create_bevel_button(second_row_frame, "连接启动", start_connection, 2, 0, 20, 5, "#43464B")

# 主事件循环模块
root.mainloop()