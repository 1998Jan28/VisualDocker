from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

import docker

# Create your views here.


def index(request):
    return render(request,'container/containerList.html')


def getClient(request):
    serverType = request.session['type']
    url = request.session['url']
    if serverType == 'local':
        return docker.from_env()
    else:
        return docker.DockerClient(url,timeout=3)

# 获取容器列表
def containerList(request):
    try:
        client = getClient(request)
        containers = client.containers.list(all=True)   # 获取容器列表
        allContainer = []
        for container in containers:
            containerInfo = {}
            containerInfo['shortId'] = container.short_id
            containerInfo['createTime'] = container.attrs['Created'].split('T')[0] + ' ' + container.attrs['Created'].split('T')[1].split('.')[0]
            containerInfo['image'] = container.image.attrs['RepoTags'][0]
            containerInfo['labels'] = container.labels
            containerInfo['name'] = container.name
            containerInfo['status'] = container.status
            containerInfo['attrs'] = container.attrs
            allContainer.append(containerInfo)
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','containers':allContainer})

# 获取指定容器详细信息
def containerInfo(request):
    try:
        client = getClient(request)
        container = client.containers.get(request.GET['containerID'])
        containerInfo = {}
        containerInfo['shortId'] = container.short_id
        containerInfo['createTime'] = container.attrs['Created'].split('T')[0] + ' ' + container.attrs['Created'].split('T')[1].split('.')[0]
        containerInfo['image'] = container.image.attrs['RepoTags'][0]
        containerInfo['labels'] = container.labels
        containerInfo['name'] = container.name
        containerInfo['status'] = container.status
        containerInfo['attrs'] = container.attrs
    except docker.errors.NotFound :
        return JsonResponse({'msg':'ContainerNotFound'})   # 该容器不存在
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','info':containerInfo})

# 运行一个新容器
def containerRun(request):
    try:
        client = getClient(request)
        imageName = request.GET['image']  # 容器的镜像
        command = request.GET['command']  # 运行容器的命令
        insidePort = request.GET['insidePort']  # 容器端口
        protocol = request.GET['protocol']  # 协议，只能是tcp,udp,sctp
        outsidePort = request.GET['outsidePort']  # 主机端口
        # e.g.  {'2222/tcp':3333} 将容器的2222端口暴露给主机的3333端口
        if insidePort == '':
            portMap = {}
        else:
            portMap = {(insidePort+protocol):int(outsidePort)}
        if command == '':
            container = client.containers.run(imageName,detach=True,ports=portMap)   # 默认在后台运行
        else:
            container = client.containers.run(imageName,command=command,detach=True,ports=portMap)
    except docker.errors.ContainerError  :
        return JsonResponse({'msg':'ContainerError'})   # 容器运行错误
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except docker.errors.ImageNotFound:
        return JsonResponse({'msg':'ImageNotFound'})  # 镜像不存在
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','containerID':container.short_id})

# 启动一个停止的容器
def containerStart(request):
    try:
        client = getClient(request)
        container = client.containers.get(request.GET['containerID'])  # 获取指定的容器
        container.start()
    except docker.errors.NotFound :
        return JsonResponse({'msg':'ContainerNotFound'})   # 该容器不存在
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success'})

# 停止一个运行的容器
def containerStop(request):
    try:
        client = getClient(request)
        container = client.containers.get(request.GET['containerID'])  # 获取指定的容器
        container.stop()
    except docker.errors.NotFound :
        return JsonResponse({'msg':'ContainerNotFound'})   # 该容器不存在
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success'})

# 重启一个运行的程序
def containerReload(request):
    try:
        client = getClient(request)
        container = client.containers.get(request.GET['containerID'])  # 获取指定的容器
        container.reload()
    except docker.errors.NotFound :
        return JsonResponse({'msg':'ContainerNotFound'})   # 该容器不存在
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success'})



