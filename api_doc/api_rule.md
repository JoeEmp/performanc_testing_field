### 响应规范

code == -1 系统级错误,一般为系统错误和传参错误

code == 0 正常

code == 1 业务错误

code == 2 同样是业务错误，方便前端做重定向

msg(具体错误信息)

### temp_api

method : post

headers

| 参数名 | 参数类型 | 是否必传 | 备注 |
| ------ | -------- | -------- | ---- |
| key    | type     | 是       | -    |

param
|参数名|参数类型|是否必传|备注|
|-|-|-|-|
|key|type|是|-|

&emsp;

请求(request case)

```js

```

响应(response case)

```json

```
