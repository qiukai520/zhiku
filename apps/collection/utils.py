from django.db.models import Q

def build_search_condition(keyword,search_fields):
    q_obj = Q()
    q_obj.connector = "OR"
    for column in search_fields:
        q_obj.children.append(("%s__icontains"%column,keyword))
    return q_obj