from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

import docker

# Create your views here.

def index(request):
    return render(request,'image/imageList.html')

def getClient(request):
    serverType = request.session['type']
    url = request.session['url']
    if serverType == 'local':
        return docker.from_env()
    else:
        return docker.DockerClient(url,timeout=3)

# 获取镜像仓库列表
def imageList(request):
    try:
        client = getClient(request)
        images = client.images.list()   # 获取镜像仓库列表
        allImage = []
        for image in images:
            imageInfo = {}
            imageInfo['shortId'] = image.short_id
            imageInfo['repoTag'] = image.attrs['RepoTags'][0]
            imageInfo['size'] = str(int(image.attrs['Size']) >> 20) + " MB"
            imageInfo['createTime'] = image.attrs['Created'].split('T')[0] + ' ' + image.attrs['Created'].split('T')[1].split('.')[0]
            imageInfo['attrs'] = image.attrs
            #print(type(image))
            #print(type(image.attrs))
            allImage.append(imageInfo)
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','images':allImage})

# 获取指定镜像详细信息
def imageInfo(request):
    try:
        client = getClient(request)
        image = client.images.get(request.GET['imageName'])
        imageInfo = {}
        imageInfo['id'] = image.id
        imageInfo['shortId'] = image.short_id
        imageInfo['tags'] = image.tags
        imageInfo['history'] = image.history()
        imageInfo['size'] = str(int(image.attrs['Size']) >> 20) + " MB"
        imageInfo['createTime'] = image.attrs['Created'].split('T')[0] + ' ' + image.attrs['Created'].split('T')[1].split('.')[0]
        imageInfo['attrs'] = image.attrs
    except docker.errors.ImageNotFound:
        return JsonResponse({'msg':'ImageNotFound'})   # 该镜像不存在
    except KeyError:
        return JsonResponse({'msg':'KeyError'})  # 参数错误
    except (docker.errors.APIError,Exception):
        return JsonResponse({'msg':'ConnectionFail'})  # 连接远程服务器失败
    return JsonResponse({'msg':'success','info':imageInfo})


