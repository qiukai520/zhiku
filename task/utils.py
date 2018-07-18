import json


def build_tags_info(dict, tags):
    tags_list = []
    for item in tags:
        tag_dict = {"name": item}
        tag_dict.update(dict)
        tags_list.append(tag_dict)
    return tags_list


def build_assign_tags_info(tasid,tags):
    tags_list = []
    for item in tags:
        tag_dict = {"tasid_id": tasid, "name": item}
        tags_list.append(tag_dict)
    return tags_list


def build_attachment_info(id_dict, attachment):
    att_list = []
    attachment = json.loads(attachment)
    for item in list(attachment):
        item.update(id_dict)
        att_list.append(item)
    return att_list


def build_assign_attach_info(tasid,attachment):
    att_list = []
    attachment = json.loads(attachment)
    for item in list(attachment):
        item.update({"tasid_id": tasid})
        att_list.append(item)
    return att_list


def build_reviewer_info(tmid, reviewers):
    re_list = []
    reviewers = json.loads(reviewers)
    for item in list(reviewers):
        item.update({"timd_id": tmid})
        re_list.append(item)
    return re_list


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

