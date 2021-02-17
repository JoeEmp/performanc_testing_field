## pay modules

- [pay](###/jmeter/pay)

### /jmeter/pay

method : post

headers

| 参数名 | 参数类型 | 是否必传 | 备注 |
| ------ | -------- | -------- | ---- |
| token  | str      | 是       | -    |

param
|参数名|参数类型|是否必传|备注|
|-|-|-|-|
|order_no|str|是|-|

&emsp;

请求(request case)

```js
var request = require("request");
var options = {
  method: "POST",
  url: "http://localhost:10086/jmeter/pay",
  headers: {
    token: "",
  },
  formData: {
    order_no: "2021021707292399",
  },
};
request(options, function (error, response) {
  if (error) throw new Error(error);
  console.log(response.body);
});
```

响应(response case)

```json
{ "code": 0, "order_no": "2021021707292399" }
```
