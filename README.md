## 安装和启动以太坊节点  

### 下载和安装geth
在官网下载并安装即可。

### 配置和启动geth
将项目geth文件夹内容复制到安装目录下，然后执行node1.bat和node2.bat可以启动预先配置好的两个以太坊节点。  
如要生成新的区块链，可以自定义编辑CustomGenesis.json文件修改初始区块信息，并将blockchaindata和blockchaindata1两个目录删除，然后执行myinit1.bat和myinit2.bat初始化节点。  

## 解决Python项目依赖
由于项目使用的是Python3.5、Flask和以太坊RPC，所以需要安装依赖包，依赖信息在写requirements.txt中。  
有两种方法：
1. 直接使用配置好的venv下的虚拟环境（windows x64, python3.5)，无需另外下载。只需执行`venv\Scripts\active.bat`。  
2. 使用pip解决依赖: 执行`pip install -r requirements.txt`，自动下载并安装依赖。  

## 数据库配置
在config.py中可以选择使用sqlite或mysql等数据库。  
如果使用mysql，需要将连接串包括账号密码替换原有的数据库连接串，并在数据控中创建好相应的数据库，表会由系统自动创建。  
如果使用sqlite，系统将会自动创建文件和表。

## 编译和部署以太坊合约
项目已编译好了智能合约并将合约信息：ABI、bytecode和合约地址储存在contract.json中。但也可以执行`python3 manage.py deploy_contract`重新部署发布新的合约，系统自动将新的合约地址保存回文件中。  
二次开发时，可以将编译好的合约二进制代码和ABI替换掉原有的并重新部署或直接替换ABI和地址直接使用。

## 启动项目
执行`python3 manage.py runserver`启动项目，默认监听5000端口。

