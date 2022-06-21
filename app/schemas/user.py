
def UserConvert(user_info_list: list) -> dict:
    return {
        'id': user_info_list[0],
        'email': user_info_list[1],
        'phone_number': user_info_list[2],
        'first_name': user_info_list[3],
        'last_name': user_info_list[4],
        'password': user_info_list[5]
    }
