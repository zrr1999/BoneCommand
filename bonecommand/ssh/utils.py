#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/7 21:41
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用

from netmiko import ConnectHandler

user_path = os.path.expanduser("~")
dev = {
    "device_type": "cisco_ios",
    "host": "1.15.231.43",
    "port": "22",
    "username": "ubuntu",
    # 'password': 'pb#qXDJrwLynccm7Cfi4ms5d',
    "use_keys": True,
    "key_file": f"{user_path}/.ssh/id_rsa",
}  # Use a dictionary to pass the login parameters

# dev = {
#     'device_type': 'cisco_ios',
#     'host': 'zrrserver.shenzhuo.vip',
#     'port': '49510',
#     'username': 'user',
#     # 'password': 'pb#qXDJrwLynccm7Cfi4ms5d',
#     'use_keys': True,
#     'key_file': f"{user_path}/.ssh/id_rsa",
# }  # Use a dictionary to pass the login parameters

# Connect to the device
router_conn = ConnectHandler(**dev)
router_conn.find_prompt()
print(router_conn.send_command("cat ~/.ssh/id_rsa.pub"))

# Send the bonecommand and print the result
