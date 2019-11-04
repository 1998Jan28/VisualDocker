from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

import docker

# Create your views here.

def index(request):
    return render(request,'login/index.html')

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

# 连接一个Docker Server
def login(request):
    try:
        serverType = request.GET['type']
        if serverType == 'local':
            client = docker.from_env()
            url = ''
        else:
            ip = request.GET['ip']
            port = request.GET['port']
            url = 'tcp://' + ip + ':' + port
            client = docker.DockerClient(url,timeout=3)
        print(client.version())
    except docker.errors.DockerException:
        return JsonResponse({'msg':'DokcerNotExist'})   # 指定的服务器上没有Docker Server
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # GET参数错误
    except Exception:
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    request.session['type'] = serverType  # 登录信息保存到session
    request.session['url'] = url
    return JsonResponse({'msg':'success'})  # 登录成功

# 获取Docker Client信息
def getClientInfo(request):
    try:
        client = getClient(request)
        versionInfo = client.version()
        dockerInfo = client.info()
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','versionInfo':versionInfo,'dockerInfo':dockerInfo})