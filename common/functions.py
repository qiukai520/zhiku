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
    # 比较参数

    final = {field: modify_info[field] for field in white_fields if field in modify_info.keys() and modify_info[field] != record[field]}

    return final