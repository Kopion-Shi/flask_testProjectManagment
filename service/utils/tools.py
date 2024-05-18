

def to_json(obj):
    dict = obj.__dict__
    if "_sa_instance_state" in dict:
        del dict["_sa_instance_state"]
        return dict