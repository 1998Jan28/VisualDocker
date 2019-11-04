from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

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

# 返回所有网络信息
def networkList(request):
    try:
        client = getClient(request)
        networks = client.networks.list()   # 获取网络列表
        allNetwork = []
        for network in networks:
            networkInfo = {}
            networkInfo['id'] = network.id
            networkInfo['name'] = network.name
            networkInfo['containers'] = network.containers
            networkInfo['attrs'] = network.attrs
            allNetwork.append(networkInfo)
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','networks':allNetwork})

# 获取指定网络信息
def networkInfo(request):
    try:
        client = getClient(request)
        network = client.networks.get(request.GET['networkId'])
        networkInfo = {}
        networkInfo['id'] = network.id
        networkInfo['name'] = network.name
        networkInfo['containers'] = network.containers
        networkInfo['attrs'] = network.attrs
    except docker.errors.NotFound :
        return JsonResponse({'msg':'NetworkNotFound'})   # 该网络不存在
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','info':networkInfo})