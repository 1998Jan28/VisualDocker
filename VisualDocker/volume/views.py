from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

import docker

# Create your views here.

import docker

# Create your views here.

def getClient(request):
    #serverType = request.session['type']
    #url = request.session['url']
    serverType = request.GET['type']
    print(serverType)
    print(serverType=='local')
    if serverType == 'local':
        return docker.from_env()
    else:
        ip = request.GET['ip']
        port = request.GET['port']
        url = 'tcp://' + ip + ':' + port
        return docker.DockerClient(url,timeout=3)

# 返回所有volume信息
def volumeList(request):
    try:
        client = getClient(request)
        volumes = client.volumes.list()   # 获取volume列表
        allVolume = []
        for volume in volumes:
            volumeInfo = {}
            volumeInfo['id'] = volume.id
            volumeInfo['name'] = volume.name
            volumeInfo['attrs'] = volume.attrs
            allVolume.append(volumeInfo)
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','volumes':allVolume})

# 获取指定volume信息
def volumeInfo(request):
    try:
        client = getClient(request)
        volume = client.volumes.get(request.GET['volumeId'])
        volumeInfo = {}
        volumeInfo['id'] = volume.id
        volumeInfo['name'] = volume.name
        volumeInfo['attrs'] = volume.attrs
    except docker.errors.NotFound :
        return JsonResponse({'msg':'VolumeNotFound'})   # 该volume不存在
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','info':volumeInfo})