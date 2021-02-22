### 业务功能

### 初始化数据

环境说明

python 3.7.0

pip 源为 aliyun

docker 提供 mysql 服务

运行下面脚本，初始化数据，会生成`csv`格式的`txt`文件供我们使用以及安装服务器的依赖

```shell
# install shell
python3 env_init.py && python3 env_init.py data
pip3 install -r requirements.txt
docker pull mysql:latest
```

start
```
docker run -itd --name pe_test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
kill -9 $(lsof -ti:10086)
nohup python3 app.py &
python3 tests/test_launch.py
```

### 文件目录结构

./

./app.py(程序入口)

./handler(接口入口，表单校验，路由转发)

./server(业务功能实现)

./com(公用基础方法)

./tests(测试含单元测试和 jmeter 的性能测试)

./api_doc(接口文档)

### 说明

0、我不是专业开发，本职还是测试。

1、服务端代码实现，有些是简化有些是简陋还有就是安全问题，请勿在生产使用。

2、不调优(主要是菜，如果有开发大佬帮忙的话再好不过.)，服务器代码提供通过单元测试。确保正常使用。

3、欢迎大家在 issue 留言,和`furnace_0xg@163.com`联系。