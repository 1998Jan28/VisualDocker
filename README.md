# Visual Docker

## 项目背景
目前对Docker的操作主要是通过终端命令交互的方式，为了简化Docker的操作，让Docker命令的运行结果更加直观，方便初学者更好的了解Docker，本项目将致力于可视化Docker。

## 项目内容
本项目主要对Docker的两个核心内容进行可视化：镜像和容器，同时也可视化展示了网络和volume的信息。
用户可以指定远程服务器或本地的Docker Server进行可视化管理。

关于镜像，项目实现了：
- 镜像仓库的展示
- 指定镜像详细信息的展示

关于容器，项目实现了：
- 所有容器展示
- 指定容器详细信息的展示
- 容器的创建、启动、终止与重启

关于网络，项目实现了：
- 网络列表的展示
- 具体网络信息的展示

关于volume，项目实现了：
- volume列表的展示
- 具体volume信息的展示

同时，还会展示指定Docker Server的相关配置信息。

## 后台接口

### 用户登录
请求地址：http://127.0.0.1:8000/login
请求方式：GET
请求参数：
- 'type' : 'local' / 'remote' (表示本地Docker或远程Docker)
- 'ip' : ip (远程主机的IP或域名，仅type为remote时需要)
- 'port' : port (远程主机端口值，仅type为remote时需要)

返回消息：
- 指定的服务器上没有Docker Server: `{'msg':'DokcerNotExist'}`
- GET参数错误：`{'msg':'KeyError'}`
- 登录成功：`{'msg':'success'}`
- 连接远程服务器失败：`{'msg':'ConnectionFail'}`

测试数据：
1.本地无Docker / ip:port错误时返回`{'msg':'DokcerNotExist'}`
http://127.0.0.1:8000/login/?type=local
http://127.0.0.1:8000/login/?type=remote&&ip=whutlcy.cn&&port=5678

2.GET参数错误`{'msg':'KeyError'}`
http://127.0.0.1:8000/login/?type=remote&&ip=whutlcy.cn

3.成功返回`{'msg':'success'}`
http://127.0.0.1:8000/login/?type=remote&&ip=whutlcy.cn&&port=5678

4.远程服务器连接失败`{'msg':'ConnectionFail'}`
http://127.0.0.1:8000/login/?type=remote&&ip=baidu.com&&port=5678

### 获取Docker信息
请求地址：http://127.0.0.1:8000/clientInfo/
返回消息：
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 连接成功：`{'msg':'success','versionInfo':versionInfo,'dockerInfo':dockerInfo}`
```json
// 其中 ... 表示省略的信息，详细信息可以自行查看
{
  "msg": "success",
  "versionInfo": {"..."},
  "dockerInfo": {"..."}
}
```

### 获取镜像仓库列表
请求地址：http://127.0.0.1:8000/image/list/
返回消息：
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 参数错误：`{'msg':'KeyError'}`
- 获取镜像仓库列表成功：`{'msg':'success','images':allImage}`

示例：http://127.0.0.1:8000/image/list/
```json
// 每个镜像的大小和创建时间attrs中也有，我已经将它们提取出来并放在最外层了
{
  "msg": "success",
  "images": [
    {
      "short_id": "sha256:540a289bab",
      "repo_tag": "nginx:latest",
      "size": "120 MB",
      "create_time": "2019-10-23 00:26:03",
      "attrs":{"..."}
    },
    {
      "short_id": "sha256:882487b8be",
      "repo_tag": "tomcat:latest",
      "size": "483 MB",
      "create_time": "2019-10-19 02:26:07",
      "attrs":{"..."}
    },
    {
      "short_id": "sha256:eb40dcf640",
      "repo_tag": "django:latest",
      "size": "415 MB",
      "create_time": "2016-12-19 16:33:54",
      "attrs":{"..."}
    }
  ]
}
```

### 获取指定镜像详细信息
请求地址：http://127.0.0.1:8000/image/list/
请求方式：GET
请求参数：
- imageName : 镜像的名称(镜像的id/shortId均可,)

返回消息：
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 参数错误：`{'msg':'KeyError'}`
- 镜像不存在：`{'msg':'ImageNotFound'}`
- 获取镜像信息成功：`{'msg':'success','info':imageInfo}`

示例：http://127.0.0.1:8000/image/info/?imageName=sha256:540a289bab
```json
{
  "msg": "success",
  "info": {
    "id": "sha256:540a289bab6cb1bf880086a9b8...",
     "shortId": "sha256:540a289bab",
    "tags": [
      "nginx:latest"
    ],
    "history": ["..."],
    "size": "120 MB",
    "createTime": "2019-10-23 00:26:03",
    "attrs": {"..."}
  }
}
```

### 获取容器列表
请求地址：http://127.0.0.1:8000/container/list
返回消息：
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 参数错误：`{'msg':'KeyError'}`
- 获取容器列表成功：`{'msg':'success','containers':allContainer}`

示例：http://127.0.0.1:8000/container/list
```json
{
  "msg": "success",
  "containers": [
    {
      "shortId": "8287fe3cc3",
      "createTime": "2019-10-25 11:44:28",
      "image": "nginx:latest",
      "labels": {
        "maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"
      },
      "name": "vigorous_hugle",
      "status": "exited",
      "attrs": {"..."}
    },
    ...
  ]
}
```

### 获取指定容器详细信息
请求地址：http://127.0.0.1:8000/container/info
请求方式：GET
请求参数：
- containerID : 容器的名称(容器的id/shortId/name均可,)

返回消息：
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 参数错误：`{'msg':'KeyError'}`
- 容器不存在：`{'msg':'ContainerNotFound'}`
- 获取容器信息成功：`{'msg':'success','info':containerInfo}`

示例：http://127.0.0.1:8000/container/info?containerID=vigorous_hugle
http://127.0.0.1:8000/container/info?containerID=8287fe3cc3
```json
// CPU和内存占用率数据均在attrs中
{
  "msg": "success",
  "info": {
    "shortId": "8287fe3cc3",
    "createTime": "2019-10-25 11:44:28",
    "image": "nginx:latest",
    "labels": {
      "maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"
    },
    "name": "vigorous_hugle",
    "status": "exited",
    "attrs": {"..."}
  }
}
```

### 运行新的容器
请求地址：http://127.0.0.1:8000/container/run/
请求方式：GET
请求参数：
- image:容器的镜像名,字符串格式(如ubuntu,nginx等)
- command：运行容器的命令(可为空)，字符串格式(如/bin/bash)
- insidePort：以下三者要么同时设置，要么都为空字符串，容器端口(0-65535)
- protocol：协议，只能是tcp,udp,sctp
- outsidePort：主机端口(0-65535)

返回消息：
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 参数错误：`{'msg':'KeyError'}`
- 镜像不存在：`{'msg':'ImageNotFound'}`
- 容器运行错误：`{'msg':'ContainerError'}`
- 获取容器信息成功：`{'msg':'success','containerID':container.short_id}`

示例：http://127.0.0.1:8000/container/run/?image=nginx&&command=&&insidePort=&&protocol=&&outsidePort=
```json
{
  "msg": "success",
  "containerID": "60b570a487"
}
```

### 容器的启动(停止运行的容器)
请求地址：http://127.0.0.1:8000/container/start/
请求方式：GET
请求参数：
- containerID : 容器的名称(容器的id/shortId/name均可,)

返回消息：
- 容器不存在：`{'msg':'ContainerNotFound'}`
- 参数错误：`{'msg':'KeyError'}`
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 容器运行成功：`{'msg':'success'}`

示例：http://127.0.0.1:8000/container/start/?containerID=60b570a487
```json
{
  "msg": "success"
}
```

### 容器的终止
请求地址：http://127.0.0.1:8000/container/stop/
请求方式：GET
请求参数：
- containerID : 容器的名称(容器的id/shortId/name均可,)

返回消息：
- 容器不存在：`{'msg':'ContainerNotFound'}`
- 参数错误：`{'msg':'KeyError'}`
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 容器终止成功：`{'msg':'success'}`

示例：http://127.0.0.1:8000/container/stop/?containerID=60b570a487
```json
{
  "msg": "success"
}
```

### 容器的重启
请求地址：http://127.0.0.1:8000/container/reload/
请求方式：GET
请求参数：
- containerID : 容器的名称(容器的id/shortId/name均可,)

返回消息：
- 容器不存在：`{'msg':'ContainerNotFound'}`
- 参数错误：`{'msg':'KeyError'}`
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 容器重启成功：`{'msg':'success'}`

示例：http://127.0.0.1:8000/container/reload/?containerID=60b570a487
```json
{
  "msg": "success"
}
```

### 获取网络列表
请求地址：http://127.0.0.1:8000/network/list/
请求方式：GET

返回消息：
- 参数错误：`{'msg':'KeyError'}`
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 获取网络列表成功：`{'msg':'success','networks':allNetwork}`

示例：http://127.0.0.1:8000/network/list/
```json
{
  "msg": "success",
  "networks": [
    {
      "id": "23d80ed4727086a0188d8572fa9220db8eeb61707b1880e5cb0782d0d5866962",
      "name": "host",
      "containers": [],
      "attrs": {
        "Name": "host",
        "Id": "23d80ed4727086a0188d8572fa9220db8eeb61707b1880e5cb0782d0d5866962",
        "Created": "2019-10-25T15:42:01.615347507+08:00",
        "Scope": "local",
        "Driver": "host",
        "EnableIPv6": false,
        "IPAM": {
          "Driver": "default",
          "Options": null,
          "Config": []
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
          "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
      }
    },
    ...
  ]
}
```

### 获取具体网络信息
请求地址：http://127.0.0.1:8000/network/info/
请求方式：GET
请求参数：
- networkId : 网络id

返回消息：
- 网络不存在：`{'msg':'NetworkNotFound'}`
- 参数错误：`{'msg':'KeyError'}`
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 获取网络信息成功：`{'msg':'success','info':networkInfo}`

示例：http://127.0.0.1:8000/network/info/?networkId=23d80ed4727086a0188d8572fa9220db8eeb61707b1880e5cb0782d0d5866962
```json
{
  "msg": "success",
  "info": {
    "id": "23d80ed4727086a0188d8572fa9220db8eeb61707b1880e5cb0782d0d5866962",
    "name": "host",
    "containers": [],
    "attrs": {
      "Name": "host",
      "Id": "23d80ed4727086a0188d8572fa9220db8eeb61707b1880e5cb0782d0d5866962",
      "Created": "2019-10-25T15:42:01.615347507+08:00",
      "Scope": "local",
      "Driver": "host",
      "EnableIPv6": false,
      "IPAM": {
        "Driver": "default",
        "Options": null,
        "Config": []
      },
      "Internal": false,
      "Attachable": false,
      "Ingress": false,
      "ConfigFrom": {
        "Network": ""
      },
      "ConfigOnly": false,
      "Containers": {},
      "Options": {},
      "Labels": {}
    }
  }
}
```

### 获取volume列表
请求地址：http://127.0.0.1:8000/volume/list/
请求方式：GET

返回消息：
- 参数错误：`{'msg':'KeyError'}`
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 获取volume列表成功：`{'msg':'success','volumes':allVolume}`

示例：http://127.0.0.1:8000/volume/list/
```json
{
  "msg": "success",
  "volumes": [
    {
      "id": "895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576",
      "name": "895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576",
      "attrs": {
        "CreatedAt": "2019-10-28T20:44:30+08:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576/_data",
        "Name": "895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576",
        "Options": null,
        "Scope": "local"
      }
    },
    {
      "id": "60442b062922efdbfdc7d3f0308b22822f53179a19fa4839c2040542a068db47",
      "name": "60442b062922efdbfdc7d3f0308b22822f53179a19fa4839c2040542a068db47",
      "attrs": {
        "CreatedAt": "2019-10-28T20:44:41+08:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/60442b062922efdbfdc7d3f0308b22822f53179a19fa4839c2040542a068db47/_data",
        "Name": "60442b062922efdbfdc7d3f0308b22822f53179a19fa4839c2040542a068db47",
        "Options": null,
        "Scope": "local"
      }
    }
  ]
}
```

### 获取具体volume信息
请求地址：http://127.0.0.1:8000/volume/info/
请求方式：GET
请求参数：
- volumeId : volumeId

返回消息：
- volume不存在：`{'msg':'VolumeNotFound'}`
- 参数错误：`{'msg':'KeyError'}`
- 连接Docker服务器失败：`{'msg':'ConnectionFail'}`
- 获取网络信息成功：`{'msg':'success','info':volumeInfo}`

示例：http://127.0.0.1:8000/volume/info/?volumeId=895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576
```json
{
  "msg": "success",
  "info": {
    "id": "895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576",
    "name": "895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576",
    "attrs": {
      "CreatedAt": "2019-10-28T20:44:30+08:00",
      "Driver": "local",
      "Labels": null,
      "Mountpoint": "/var/lib/docker/volumes/895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576/_data",
      "Name": "895fe034bc684c29dffa40615069d17b375ee8bf213941d31de287800c9ef576",
      "Options": null,
      "Scope": "local"
    }
  }
}
```