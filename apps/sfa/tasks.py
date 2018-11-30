
# Create your tasks here

import datetime

from thinking_library.celery import app
from sfa.server import customer_db
from .server import sea_rule_db

@app.task
def check_customer():
    """自动审查客户签约状态"""
    sea_rule = 15
    rule_obj = sea_rule_db.query_rule()
    if rule_obj:
        sea_rule = rule_obj.rule
    now_time = datetime.datetime.today()
    # 获取过期客户
    expire_time = now_time - datetime.timedelta(sea_rule)
    customer_list = customer_db.query_customer_by_is_sign(0, expire_time)
    for item in customer_list:
        from django.db import connection, connections
        cursor = connection.cursor()  # cursor = connections['default'].cursor()
        cursor.execute("""update customer_info SET follower_id = 0 where nid = %s""", [item.nid])
        cursor.close()



