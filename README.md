

# TPShow

快速查询TPLink路由器信息的小模块

## 目录

- [安装指南](#安装指南)
  - [适用环境](#适用环境)
  - [安装步骤](#安装步骤)

### 安装指南

#### 开发前的配置要求
![s](s.png)

测试过的型号
1、TL-WAR1200L

理论上支持部分图中这种页面的TPLink路由器

#### **安装步骤**

1. 克隆项目
2. 进入到项目目录
3. 安装依赖
```sh
pip install -r requirements.txt
```
4. 安装模块
```sh
pip install .
```
5. 输入`TPShow`运行测试
```sh
请输入IP:192.168.3.1
请输入用户名:admin
请输入密码:xxxxxx
Token 获取成功: 8xxxxxxxxxx8d4179a426b1
路由器状态信息已获取
Combined Router Data
     Port  Link Speed (Mbps) Interface Online Status Memory Usage (%) CPU Usage (%)
0  port_1               1000      WAN1        Online               63            16
1  port_2               1000      WAN2        Online               63            16
2  port_3                  0  VPN_WAN1       Offline               63            16
3  port_4                  0      None          None               63            16
4  port_5               1000      None          None               63            16
```



