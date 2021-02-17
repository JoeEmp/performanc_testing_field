docker run -itd --name pe_test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
kill -9 $(lsof -ti:10086)
nohup python3 app.py &
jmeter -t ./tests/api_test.jmx
