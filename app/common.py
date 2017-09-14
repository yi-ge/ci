def trueReturn(data, msg):
    return {
        "status": 1,
        "result": {
            "data": data,
            "msg": msg
        }
    }


def falseReturn(code, data, msg):
    return {
        "status": code,
        "result": {
            "data": data,
            "msg": msg
        }
    }
