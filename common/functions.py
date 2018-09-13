import json
from datetime import date
from datetime import datetime


class CJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
# dl= json.dumps(datalist, cls=JsonCustomEncoder)


def filter_fields(white_fields, modify_info):
    # 过滤参数 （非空）

    final = {field: modify_info[field] for field in white_fields if field in modify_info.keys()
             and modify_info[field]}

    return final


def compare_fields(white_fields, record, modify_info):
    # 比较参数,并去掉字符串多余空格
    final = {field:  modify_info[field].strip() if type(modify_info[field]) == str else modify_info[field] for field in white_fields if field in modify_info.keys() and modify_info[field] != getattr(record,field)}
    return final


def compare_json(record, modify_info, id_key):
    # json 数据对比
    id_key = str(id_key)
    insert_list = []
    update_list = []
    update_id_list = []
    delete_list_id_list = []
    for item in modify_info:
        id = item.get(id_key,None)
        if id:
             update_id_list.append(int(id))
             update_list.append(item)
        else:
            insert_list.append(item)
    for item in record:
        key = getattr(item, id_key)
        if int(key) not in update_id_list:
            delete_list_id_list.append(item.pk)
    return insert_list, update_list, delete_list_id_list


def build_attachment_info(id_dict, attachment_list):
    att_list = []
    for item in attachment_list:
        item.update(id_dict)
        att_list.append(item)
    return att_list