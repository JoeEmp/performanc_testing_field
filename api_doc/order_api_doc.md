## order module

- [add](###/jmeter/app/order/add)
- [detail](###/jmeter/app/order/detail)
- [list](###/jmeter/app/order/list)

### /jmeter/app/order/add

method : post

headers

| 参数名 | 参数类型 | 是否必传 | 备注 |
| ------ | -------- | -------- | ---- |
| token  | str      | 是       | -    |

param
|参数名|参数类型|是否必传|备注|
|-|-|-|-|
|good_ids|str|是|列表字符串|

&emsp;

请求(request case)

```js
var request = require("request");
var options = {
  method: "POST",
  url: "http://localhost:10086/jmeter/app/order/add",
  headers: {
    token: "",
  },
  formData: {
    good_ids: "[3]",
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

### /jmeter/app/order/detail

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
  url: "http://localhost:10086/jmeter/app/order/detail",
  headers: {
    token: "",
  },
  formData: {
    order_no: "2021021607002465",
  },
};
request(options, function (error, response) {
  if (error) throw new Error(error);
  console.log(response.body);
});
```

响应(response case)

```json
{
  "code": 0,
  "order": {
    "id": 2,
    "username": "nliu@yahoo.com",
    "order_no": "2021021706279672",
    "good_ids": "3",
    "pay_id": null,
    "sum_price": 5993,
    "status": 3,
    "create_time": "2021-02-17 14:27:11",
    "update_time": "2021-02-17 14:27:11"
  }
}
```

### /jmeter/app/order/list

method : post

headers

| 参数名 | 参数类型 | 是否必传 | 备注 |
| ------ | -------- | -------- | ---- |
| token  | str      | 是       | -    |

param
|参数名|参数类型|是否必传|备注|
|-|-|-|-|
|page|int|否|默认为 1|
|page_size|int|否|默认为 10|
|sorts_by|list|否|1 为降序,0 为升序,排序关键字为表字段|

&emsp;

请求(request case)

```js
var request = require("request");
var options = {
  method: "POST",
  url: "http://localhost:10086/jmeter/app/order/list",
  headers: {
    token: "",
  },
  formData: {
    page: "1",
    page_size: "1",
    sorts_by: "[['id','1']]",
  },
};
request(options, function (error, response) {
  if (error) throw new Error(error);
  console.log(response.body);
});
```

响应(response case)

```json
{
  "code": 0,
  "list": [
    {
      "id": 147,
      "username": "nliu@yahoo.com",
      "order_no": "2021021707443698",
      "good_ids": "2",
      "pay_id": "wxbv5nlVKrui9j1CDLmRxqokMeUzNsIZS3",
      "sum_price": 4322,
      "status": 1,
      "create_time": "2021-02-17 15:44:42",
      "update_time": "2021-02-17 15:44:42"
    }
  ]
}
```
