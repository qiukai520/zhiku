import json
def build_tags_info(tid, tags):
    tags_list = []
    for item in tags:
        tag_dict = {"tid": tid, "name": item}
        tags_list.append(tag_dict)
    return tags_list


def build_attachment_info(tid, attachment):
    att_list = []
    attachment = json.loads(attachment)
    for item in list(attachment):
        item.update({"tid": tid})
        att_list.append(item)
    return att_list


def build_reviewer_info(tid, reviewers):
    re_list = []
    reviewers = json.loads(reviewers)
    for item in list(reviewers):
        item.update({"tid": tid})
        re_list.append(item)
    return re_list


def compare_json(record, modify_info, id_key):
    #json 数据对比
    id_key = str(id_key)
    print(type(id_key))
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
        print("id_key", getattr(item, id_key))
        print(id_key)
        key = getattr(item, id_key)
        if int(key) not in update_id_list:
            delete_list_id_list.append(item.pk)
    print(insert_list,update_list,delete_list_id_list)
    return insert_list, update_list, delete_list_id_list



# def compare_json(record, modify_info, dict_keys=[]):
#     # json数据对比
#
#     record = list_cover_key_dict(record, dict_keys)
#     modify_info = list_cover_key_dict(modify_info, dict_keys)
#
#     insert_lists = [modify_info[key] for key in modify_info.keys() if key not in record.keys()]
#     delete_lists = [record[key] for key in record.keys() if key not in modify_info.keys()]
#     record_lists = {key: record[key] for key in record.keys() if key in modify_info.keys()}
#     update_lists = {key: modify_info[key] for key in modify_info.keys() if key in record.keys()}
#
#     return insert_lists, delete_lists, record_lists, update_lists
#
#
# def list_cover_key_dict(record, dict_keys=[]):
#     # 列表转成带组合key的dict
#
#     if not dict_keys:
#         return {}
#
#     # 格式化
#     final = {generate_str(item, dict_keys): item for item in record}
#
#     return final