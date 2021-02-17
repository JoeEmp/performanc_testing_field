## login modules

- [login](###/jmeter/login)

### /jmeter/login

method : post

param
|参数名|参数类型|是否必传|备注|
|-|-|-|-|
|username|str|是|-|
|password|str|是|-|

&emsp;

请求(request case)

```js
var request = require("request");
var options = {
  method: "POST",
  url: "http://localhost:10086/jmeter/login",
  headers: {},
  formData: {
    username: "nliu@yahoo.com",
    password: "f18581cea866c3ddaaa3c39277e5d87d",
  },
};
request(options, function (error, response) {
  if (error) throw new Error(error);
  console.log(response.body);
});
```

响应(response case)

```json
{ "code": 0, "token": "213" }
```
