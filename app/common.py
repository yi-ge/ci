def trueReturn(data, msg):
    return {
        "status": 1,
        "result": {
            "data": data,
            "msg": msg
        }
    }


def falseReturn(data, msg):
    return {
        "status": 50000,
        "result": {
            "data": data,
            "msg": msg
        }
    }
