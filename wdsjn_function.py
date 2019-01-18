import Levenshtein
import re


def parse_command(command, desc):
    functions_desc = desc['functions']
    device_types_desc = desc['device_types']
    devices_desc = desc['devices']
    rooms_desc = desc['rooms']

    command = command.lower()

    words = command.split()
    error, devices = find_devices_in_room_catch(rooms_desc, words)
    if error:
        return devices
    error, device_type = get_device_type_catch(devices, devices_desc, device_types_desc, words)
    if error:
        return device_type
    error, device_id = get_device_id_catch(devices, devices_desc, device_type, words)
    if error:
        return device_id
    error, func = get_fun_catch(device_type, device_types_desc, functions_desc, words)
    if error:
        return func

    try:
        output = functions_desc[func]['output']
        result = output.replace('{id}', device_id)
        if 'placeholder' in functions_desc[func] and functions_desc[func]['placeholder']:
            regex = functions_desc[func]['regex']
            for reg in regex:
                reg_value = regex[reg]['value']
                reg_result = re.findall(str(reg_value), command)
                if len(reg_result) > 0:
                    placeholder = reg_result[0]
                    if ('identity' not in regex[reg] or not regex[reg]['identity']) \
                            and 'translation' in regex[reg]:
                        placeholder = regex[reg]['translation']
                    result = result.replace('{placeholder}', str(placeholder))
                    break
    except:
        return 'error'

    return result


def get_fun(device_type, device_types_desc, functions_desc, words, threshold=0.95):
    max_sum = 0
    max_len = 0
    max_fun = None
    device_type_desc = device_types_desc[device_type]
    for fun in device_type_desc['functions']:
        fun_desc = functions_desc[fun]

        if max_fun is None and 'default' in fun_desc and fun_desc['default']:
            max_fun = fun

        for alias in fun_desc['aliases']:
            alias_sum = 0
            alias_words = alias.split()
            current_len = len(alias_words)
            for alias_word in alias_words:
                for word in words:
                    rate = Levenshtein.ratio(alias_word, word)
                    alias_sum += rate if rate > threshold else 0
            if alias_sum > max_sum:
                max_sum = alias_sum
                max_len = current_len
                max_fun = fun
            elif alias_sum == max_sum and current_len < max_len:
                max_len = current_len
                max_fun = fun
    return max_fun


def get_fun_catch(device_type, device_types_desc, functions_desc, words, threshold=0.95):
    try:
        return False, get_fun(device_type, device_types_desc, functions_desc, words, threshold)
    except:
        return True, 'error'


def get_device_id(devices, devices_desc, device_type, words, threshold=0.65):
    max_sum = 0
    max_len = 0
    max_id = None

    for device in devices:
        device_desc = devices_desc[device]
        if device_desc['type'] == device_type:
            if 'aliases' in device_desc:
                for alias in device_desc['aliases']:
                    alias_sum = 0
                    alias_rate = 0
                    alias_words = alias.split()
                    current_len = len(alias_words)
                    for alias_word in alias_words:
                        for word in words:
                            rate = Levenshtein.ratio(alias_word, word)
                            alias_rate += 1 if rate > threshold else 0
                            alias_sum += rate if rate > threshold else 0
                    if alias_rate < current_len:
                        alias_sum = 0
                    if alias_sum > max_sum:
                        max_sum = alias_sum
                        max_len = current_len
                        max_id = device
                    elif alias_sum == max_sum and current_len < max_len:
                        max_len = current_len
                        max_id = device
                    elif alias_sum == max_sum and 'default' in device_desc and device_desc['default']:
                        max_sum = 0
                        max_len = 0
                        max_id = device
            if max_id is None:
                max_id = device
                max_sum = 0
                max_len = 0

    return max_id


def get_device_id_catch(devices, devices_desc, device_type, words, threshold=0.65):
    try:
        return False, get_device_id(devices, devices_desc, device_type, words, threshold)
    except:
        return True, 'error'


def get_device_type(devices, devices_desc, device_types_desc, words, threshold):
    possible_types = set([devices_desc[device]['type'] for device in devices])

    max_sum = 0
    max_len = 0
    max_type = None
    for d_type in possible_types:
        device_desc = device_types_desc[d_type]
        for alias in device_desc['aliases']:
            alias_sum = 0
            alias_words = alias.split()
            current_len = len(alias_words)
            for alias_word in alias_words:
                for word in words:
                    rate = Levenshtein.ratio(alias_word, word)
                    alias_sum += rate if rate > threshold else 0
            if alias_sum > max_sum:
                max_sum = alias_sum
                max_len = current_len
                max_type = d_type
            elif alias_sum == max_sum and current_len < max_len:
                max_len = current_len
                max_type = d_type

    return max_type


def get_device_type_catch(devices, devices_desc, device_types_desc, words, threshold=0.70):
    try:
        return False, get_device_type(devices, devices_desc, device_types_desc, words, threshold)
    except:
        return True, 'error'


def find_devices_in_room(rooms, words, threshold=0.65):
    max_sum = 0
    max_len = 0
    max_v = None
    for room_desc in rooms:
        for _, v in room_desc.items():
            for alias in v['aliases']:
                alias_sum = 0
                alias_words = alias.split()
                current_len = len(alias_words)
                for alias_word in alias_words:
                    for word in words:
                        rate = Levenshtein.ratio(alias_word, word)
                        alias_sum += rate if rate > threshold else 0
                if alias_sum > max_sum:
                    max_sum = alias_sum
                    max_len = current_len
                    max_v = v
                elif alias_sum == max_sum and current_len < max_len:
                    max_len = current_len
                    max_v = v
    return max_v['devices']


def find_devices_in_room_catch(rooms, words, threshold=0.65):
    try:
        return False, find_devices_in_room(rooms, words, threshold)
    except:
        return True, 'error'
