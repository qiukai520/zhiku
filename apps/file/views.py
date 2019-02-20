import json
import os
import uuid
import hashlib
from django.db import transaction
from django.shortcuts import render,HttpResponse
from .server import *
# Create your views here.


def add_tag(request):
    ret = {"status":False,"data":"","message":''}
    name = request.POST.get("tag_name",'')
    if name:
        try:
            tag_db.insert_tag({"name":name})
            ret["status"] = True
        except Exception as e:
            print(e)
            ret["message"] = e
    return HttpResponse(json.dumps(ret))


def manager(request):
    file_list = file_db.query_file_list()
    return render(request,"file/file_manager.html",{"query_set":file_list})


def check_chunk(request):

    """判断该文件上传了多少个分片"""
    target_path = "media/file"
    name = request.POST.get('fileName')
    chunk = 0
    data = {}
    filename = target_path+"/%s" % name

    # 判断上传的文件是否存在
    if os.path.exists(filename):
        data['flag_exist'] = True
        data['file_path'] = filename
    else:
        data['flag_exist'] = False
    list = []
    while True:
        if os.path.exists(target_path+'/{}-{}'.format(name, chunk)):
            list.append(chunk)
        else:
            break
        chunk += 1
    data['list'] = list
    return HttpResponse(json.dumps({'ifExist':False}))


def merge_chunks(request):
    target_path = "media/file"
    owner = request.user.staff.sid
    classify = request.POST.get('classify')
    tags = request.POST.get('tags')
    tags_list = tags.split("|")
    size = request.POST.get("fileSize")
    name = request.POST.get('fileName')
    md5 = request.POST.get('fileMd5')
    print("size",size)
    print("name",name)
    print("md5",md5)
    chunk = 0  # 分片序号
    temp_filename = os.path.join(target_path,  str(uuid.uuid1()))
    digest = hashlib.sha1()
    with open(temp_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = target_path+'/{}-{}'.format(md5, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                digest.update(source_file.read())
                source_file.close()
            except IOError as e:
                # 找不到碎片文件跳出循环
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
        target_file.close()
    # 存入数据库
    digest = digest.hexdigest()  # hash 对象转字符串
    file_path = os.path.join(target_path, digest)
    # os.path.join()在Linux/macOS下会以斜杠（/）分隔路径，而在Windows下则会以反斜杠（\）分隔路径,
    # 故统一路径将'\'替换成'/'
    file_path = file_path.replace('\\', "/")

    # 存到数据库
    file_info = {
        "name": name,
        "path": file_path,
        "size":size,
        "digest":digest,
        "owner_id":owner,
        "classify":classify,
    }
    with transaction.atomic():
        try:
            fid = file_db.insert_file(file_info)
            array = []
            for item in tags_list:
                array.append({"tag_id":int(item),"file_id":fid})
            file2tag_db.mutil_insert(array)
        except Exception as e:
            print(e)
    if not os.path.exists(file_path):
        os.rename(temp_filename, file_path)
    return HttpResponse(json.dumps({'upload':True,"data":file_path}))


def upload(request):  # 接收前端上传的一个分片
    target_path = "media/file"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    md5 = request.POST.get('fileMd5')
    chunk_id = request.POST.get('chunk',0)
    filename = '{}-{}'.format(md5,chunk_id)
    upload_file = request.FILES.get("file")
    file_path = os.path.join(target_path,filename)
    file_path = file_path.replace('\\', "/")
    if not os.path.exists(file_path):
        try:
            with open(file_path, 'wb') as f:
                # for obj in upload_file.chunks():
                #     f.write(obj)
                f.write(upload_file.read())
                f.close()
        except Exception as e:
            pass
    # upload_file.save(target_path+'/{}'.format(filename))
    return HttpResponse(json.dumps({'upload_part':True}))