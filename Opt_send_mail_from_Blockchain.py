# -*- coding:UTF-8 -*-
from web3 import Web3,HTTPProvider
import os
import time
import binascii
import base64
import smtplib
from email.mime.text import MIMEText
from email.header import Header

contract_address = "0xF8dCbDcbc61752E95d9AB23b38fB79674c9A8FB6" # 你的合约地址
contract_topic0 = "0x90c04e3c5f60e054d780a4cf893b5797e089c3da43565f81a1146044d51e8a11" # 事件日志中的topic0，针对同意合约的所有事件日志的topic0都是相同的
rpc = "https://ropsten.infura.io/v3/da.....2d7" # 你注册的Infura中的ENDPOINT


flag = "flag{a_smart_contract_test}"
email = {
    "host":"smtp.163.com",
    "port":25,
    "user":"aaaaa@163.com", # 用来发送flag的邮箱
    "code":"aaaaa"  # 邮箱的客户端授权码
}
# initial
w3 = Web3(Web3.HTTPProvider(rpc))
sender = smtplib.SMTP(host=email["host"],port=email["port"])
sender.ehlo()
sender.starttls()
sender.login(email["user"],email["code"])

# email content
message = MIMEText("收下你的flag:"+flag, 'plain', 'utf-8')
message["From"] = email["user"]
message["Subject"] = Header("ctf flag","utf-8")

# 发送flag的函数
def sendflag(toEmail):
    message["To"] = toEmail
    sender.sendmail(email["user"],toEmail,message.as_string())
    # log
    os.system("echo "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +": Get flag -- "+toEmail+" >> /tmp/variant_of_cat.log")
    print("send success")

# 监听合约事件的函数

def event():
    # 从网络中的事件日志中抓取符合这一合约的日志信息
    flag_logs = w3.eth.getLogs({
            "address":contract_address,
            "topic0":contract_topic0
        })
    if flag_logs is not []:
        for flag_log in flag_logs:
            data = flag_log["data"][2:]
            length = int(data[64*2:64*3].replace('00', ''),16)
            data = data[64*3:][:length*2]
            b64email = binascii.unhexlify(data).decode('utf-8')
            try:
                #print(dict.get(b64email))
                if dict.get(b64email)==None:# 防止重复发送
                    print(b64email)
                    sendflag(b64email)
                    dict[b64email]=1
            except Exception as e:
                errmsg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+":decode or send to b64 - {} fail".format(b64email)
                os.system("echo " + errmsg +str(e) + ">> /tmp/variant_of_cat_error.log")
                print(errmsg+str(e))
# 循环运行
dict={}
while(True):
    event()
    