import json
import requests
import pandas as pd

def au(a):
    return security_encode(a, "RDpbLfCPsJZ7fiv", "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW")

def security_encode(a, b, e):
    f = ""
    k, u = 187, 187  # Initialize k and u to 187 as in the JavaScript code
    h = len(a)  # Length of string 'a'
    m = len(b)  # Length of string 'b'
    d = len(e)  # Length of string 'e'
    
    # Determine the maximum length
    g = max(h, m)
    
    # Iterate over each character position up to the length 'g'
    for l in range(g):
        u = k = 187  # Reset k and u to 187 at each iteration
        
        if l >= h:
            u = ord(b[l])  # If l exceeds 'a', use character from 'b'
        elif l >= m:
            k = ord(a[l])  # If l exceeds 'b', use character from 'a'
        else:
            k = ord(a[l])  # Otherwise, use both characters
            u = ord(b[l])
        
        # Append the encoded character to the result string
        f += e[(k ^ u) % d]
    
    return f

# 汇总数据到一个表格中
def generate_combined_table(status_info):
    # 初始化表格的列
    combined_data = {
        'Port': [],
        'Link Speed (Mbps)': [],
        'Interface': [],
        'Online Status': [],
        'Memory Usage (%)': [],
        'CPU Usage (%)': []
    }

    # 处理 port 相关信息
    port_count = 0
    if 'port' in status_info:
        for port_if in status_info['port']['port']:
            for port_key, port_info in port_if.items():
                if 'port_' in port_key:
                    speed = port_info['link_speed']
                    combined_data['Port'].append(port_key)
                    combined_data['Link Speed (Mbps)'].append(0 if speed == "---" else int(speed.replace("M", "").strip()))
                    port_count += 1
                else:
                    combined_data['Port'].append(port_key)
                    combined_data['Link Speed (Mbps)'].append(None)  # 没有速率的端口

    # 处理在线设备信息
    online_count = 0
    if 'online_check' in status_info:
        for i in range(status_info['online_check']['count']['state']):
            state_key = f'state_{i + 1}'
            if state_key in status_info['online_check']['state']:
                state_info = status_info['online_check']['state'][state_key]
                combined_data['Interface'].append(state_info['if'])
                combined_data['Online Status'].append("Online" if state_info['state'] == "up" else "Offline")
                online_count += 1

    # 处理系统内存与CPU使用情况
    if 'system' in status_info:
        mem_usage = status_info['system']['mem_usage']['mem']
        core1_usage = status_info['system']['cpu_usage']['core1']
    else:
        mem_usage = None
        core1_usage = None

    # 计算需要填充的行数，使所有列长度相等
    max_length = max(len(combined_data['Port']), len(combined_data['Interface']))

    # 填充 Port 和 Link Speed 数据列
    if len(combined_data['Port']) < max_length:
        combined_data['Port'].extend([None] * (max_length - len(combined_data['Port'])))
        combined_data['Link Speed (Mbps)'].extend([None] * (max_length - len(combined_data['Link Speed (Mbps)'])))

    # 填充 Interface 和 Online Status 数据列
    if len(combined_data['Interface']) < max_length:
        combined_data['Interface'].extend([None] * (max_length - len(combined_data['Interface'])))
        combined_data['Online Status'].extend([None] * (max_length - len(combined_data['Online Status'])))

    # 填充 Memory Usage 和 CPU Usage 数据列
    combined_data['Memory Usage (%)'] = [mem_usage] * max_length
    combined_data['CPU Usage (%)'] = [core1_usage] * max_length

    # 将所有数据转化为DataFrame
    combined_table = pd.DataFrame(combined_data)
    return combined_table


def main():
    # 路由器的 IP 地址
    router_ip = input("请输入IP:")  # 替换为您的路由器 IP 地址
    username= input("请输入用户名:")
    password = au(input("请输入密码:"))
    login_url = f"http://{router_ip}/"  # 登录的 URL
    login_data = {
        "method": "do",
        "login": {
            "username": username,  # 替换为实际用户名
            "password": password  # 替换为实际密码
        }
    }


    # 发送POST请求进行登录
    session = requests.Session()
    login_response = session.post(login_url, json=login_data)

    # 提取stok (token)
    try:
        stok = json.loads(login_response.text)['stok']
        print(f"Token 获取成功: {stok}")
    except KeyError:
        print("未能获取 token，检查登录响应内容。")
        print("响应内容:", login_response.text)
        exit()

    # 准备获取路由器状态的请求
    status_url = f"http://{router_ip}/stok={stok}/ds"
    status_data = {
        "method": "get",
        "network": {
            "name": "if_mode",
            "table": "if_info",
            "filter": [
                {
                    "base_name": [
                        "lan",
                        "wan1_eth",
                        "wan2_eth"
                    ]
                }
            ]
        },
        "online_check": {
            "table": "state"
        },
        "qos": {
            "table": "interface"
        },
        "dhcpd": {
            "table": "dhcpd_list"
        },
        "port": {
            "table": "port"
        },
        "system": {
            "table": "ifstat_list",
            "name": [
                "cpu_usage",
                "mem_usage"
            ]
        },
        "wireless": {
            "name": [
                "wlan_host_2g",
                "wlan_host_5g"
            ],
            "table": [
                "cur_channel",
                "wlan_wds",
                "sta_list"
            ],
            "filter": [
                {
                    "radio_id": "1"
                },
                {
                    "radio_id": "2"
                }
            ]
        },
        "guest_network": {
            "name": "guest_2g"
        }
    }

    # 发送获取状态的请求
    status_response = session.post(status_url, json=status_data)

    # 解析返回的数据
    if status_response.status_code == 200:
        status_info = json.loads(status_response.content)
        print("路由器状态信息已获取")
    else:
        print(f"获取状态信息失败，状态码: {status_response.status_code}")
        print("响应内容: ", status_response.content)
        exit()

    # 生成并展示汇总表格
    combined_table = generate_combined_table(status_info)

    # 使用 ace_tools.display_dataframe_to_user 展示表格
    import ace_tools_open as tools
    tools.display_dataframe_to_user("Combined Router Data", combined_table)
