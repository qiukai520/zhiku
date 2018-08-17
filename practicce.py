target_path = "static/upload/task"
import os
if not os.path.exists(os.path.dirname(target_path)):
    print("not")
    os.makedirs(target_path)