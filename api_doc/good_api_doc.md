## good module

- [detail](###/jmeter/app/good/detail)
- [list](###/jmeter/app/good/list)

### /jmeter/app/good/detail

method : post

param
|参数名|参数类型|是否必传|备注|
|-|-|-|-|
|id|int|是|商品 id|

&emsp;

请求(request case)

```js
var request = require("request");
var options = {
  method: "POST",
  url: "http://localhost:10086/jmeter/app/good/detail",
  headers: {},
  formData: {
    id: "2",
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
  "good": {
    "id": 2,
    "name": "飞鹤奶粉",
    "inventory": 4299,
    "price": 4322,
    "create_time": "2021-02-17 13:34:38",
    "update_time": "2021-02-17 15:44:42"
  }
}
```

### /jmeter/app/good/list

method : post

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
  url: "http://localhost:10086/jmeter/app/good/list",
  headers: {
    token: "",
  },
  formData: {
    page: "1",
    page_size: "2",
    sorts_by: "[['id','1'],['inventory','0']]",
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
  "goods": [
    {
      "id": 2,
      "name": "飞鹤奶粉",
      "inventory": 4299,
      "price": 4322,
      "create_time": "2021-02-17 13:34:38",
      "update_time": "2021-02-17 15:44:42"
    },
    {
      "id": 3,
      "name": "2022款 MacbookAir M1 全网最低",
      "inventory": 457,
      "price": 5993,
      "create_time": "2021-02-17 13:34:38",
      "update_time": "2021-02-17 16:43:45"
    }
  ]
}
```
