import requests
import os
import json
from datetime import datetime
import time
import warnings
from core.config import configs
warnings.filterwarnings("ignore")
# 设置 NiFi 的地址和端口
nifi_url = configs.NIFI_URL
auth_url = f'{nifi_url}/access/token'

# 认证信息
username = 'admin'
password = 'WeiQiao@pa4word'

# 获取访问令牌
def get_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': configs.NIFI_USERNAME,
        'password': configs.NIFI_PASSWORD
    }
    response = requests.post(auth_url, headers=headers, data=data, verify=False)
    if response.status_code == 201:
        return response.text
    else:
        raise Exception(f"Failed to get token: {response.status_code} - {response.text}")

# 获取公告信息
def get_bulletin_board(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = f'{nifi_url}/flow/bulletin-board'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get message: {response.status_code} - {response.text}")

#获取处理器组信息
def get_processor_group_information(token, id):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = f'{nifi_url}/flow/process-groups/{id}'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get processor group information: {response.status_code} - {response.text}")


def send_dingding_message(message):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "NiFi报警信息",
            "text": message
        }
    }
    url = configs.DINGROBOT_ZHONGTAI
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to send message: {response.status_code} - {response.text}")
    
def get_error_message(all_message):
    error_message = []
    for message in all_message['bulletinBoard']['bulletins']:
        # 如果message有bulletin字段，则为节点报警信息，否则为系统报警信息
        if 'bulletin' in message and message['bulletin']['level'] == 'ERROR':
            error_message.append(message['bulletin'])
    return error_message

def filter_repeated_message(error_message):
    filtered_error_message = []
    remaining_error_message = []

    # 如果category 不是'Log Message'则直接加入错误信息
    for error in error_message:
        if error['category'] != 'Log Message':
            filtered_error_message.append(error)
        else:
            remaining_error_message.append(error)

    remaining_error_message = sorted(remaining_error_message, key=lambda x: x['sourceId'])
    duplicate_count = 1

    if len(remaining_error_message) == 1:
        remaining_error_message[0]['duplicate_count'] = duplicate_count
        filtered_error_message.append(remaining_error_message[0])
        return filtered_error_message

    for i in range(len(remaining_error_message) - 1):
        if remaining_error_message[i]['sourceId'] == remaining_error_message[i + 1]['sourceId']:
            duplicate_count += 1
        else:
            remaining_error_message[i]['duplicate_count'] = duplicate_count
            filtered_error_message.append(remaining_error_message[i])
            duplicate_count = 1

    if remaining_error_message:
        remaining_error_message[-1]['duplicate_count'] = duplicate_count
        filtered_error_message.append(remaining_error_message[-1])

    return filtered_error_message

#递归解析父目录名
def get_parent_name(parentBreadcrumb):
    if 'parentBreadcrumb' not in parentBreadcrumb:
        return parentBreadcrumb['breadcrumb']['name']
    else:
        return get_parent_name(parentBreadcrumb['parentBreadcrumb']) + '>>' + parentBreadcrumb['breadcrumb']['name']


#根据组件ID获取处理器所在路径信息
def transform_message_by_groupid(token,error_message):
    message = ''
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    error_message = sorted(error_message, key=lambda x: x['sourceId'])
    count = 1
    group_id_set = set()
    for error in error_message:
        #第一次进入循环则加入标题
        if count == 1:
            message += f"### NiFi报警信息汇总 ### \n"
        if error['category'] == 'Log Message':
            if error['groupId'] in group_id_set:
                continue
            group_id_set.add(error['groupId'])
            group_information = get_processor_group_information(token, error['groupId'])
            breadcrumb = group_information['processGroupFlow']['breadcrumb']
            child_name = breadcrumb['breadcrumb']['name']
            #如果组件的父组件不为空，则地址名为解析后的父组件名+子组件名
            parent_name = get_parent_name(breadcrumb['parentBreadcrumb'])
            group_name = ''
            if parent_name != '':
                group_name = parent_name + '>>' + child_name
            else:
                group_name = child_name
            message += f"{count}. **报警时间:** {date} {error['timestamp']}  \n"
            message += f"**报警位置:** {group_name}\n"
        else:
            message += f"{count}. **报警时间:** {date} {error['timestamp']}  \n"
            message += f"**节点地址:** {error['nodeAddress']}   \n"
        #清空set
        count += 1
    group_id_set.clear()
    return message

# 主函数
def nifi_alarm_to_dingding():
    # 获取令牌
    try:
        token = get_token()
        all_message = get_bulletin_board(token)
        # 获取错误信息
        error_mesage = get_error_message(all_message)
        # 过滤同一个组件的重复报警信息, 只保留一个,增加报警次数字段
        filtered_error_message = filter_repeated_message(error_mesage)
        # 钉钉消息格式化
        dingding_message = transform_message_by_groupid(token,filtered_error_message)
        print(dingding_message)
        # 如果错误信息不为空发送钉钉消息
        if dingding_message != '':
            response = send_dingding_message(dingding_message)
            print(response)
        print('nifi监控程序运行成功')
    except Exception as e:
        print(e)
