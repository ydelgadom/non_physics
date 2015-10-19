import json


def convert_to_json(dict_):
    """
    convert string to json
    """
    output = {}
    for key in dict_:
        try:
            output[key] = json.loads(dict_[key])
        except:
            output[key] = dict_[key]
    return output


def convert_list_to_json(list_):
    """
    convert string to json
    """
    output = list()
    for item in list_:
        output.append(convert_to_json(item))
    return output
