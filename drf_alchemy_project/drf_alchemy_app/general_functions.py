def success_message(data=0):
    response_dictionary = dict()
    response_dictionary["is_success"] = True
    response_dictionary["data"] = data
    return response_dictionary


def error_message(data=0):
    response_dictionary = dict()
    response_dictionary["is_success"] = False
    response_dictionary["data"] = data
    return response_dictionary
