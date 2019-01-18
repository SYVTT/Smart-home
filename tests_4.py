import yaml


from bcolors import bcolors
from test_cases_original import test_cases_original
from wdsjn_function import parse_command


if __name__ == "__main__":
    formal_language = yaml.load(open('V_4.yaml'))

    total_correct = total_wrong = 0
    for (command, expected) in test_cases_original:
        result = None
        try:
            result = parse_command(command, formal_language)
        except:
            total_wrong += 1
        if result not in expected:
            print(bcolors.FAIL + 'result = ' + str(result) + ' | expected = ' + str(expected) + bcolors.ENDC
                  + ' in sentence: ' + command)
            total_wrong += 1
        else:
            print(bcolors.OKGREEN + 'result = expected = ' + str(expected) + bcolors.ENDC
                  + ' in sentence: ' + command)
            total_correct += 1

    print('\n')
    print('total = ' + str(len(test_cases_original)))
    print(bcolors.OKGREEN + 'total correct = ' + str(total_correct) + bcolors.ENDC)
    print(bcolors.FAIL + 'total wrong = ' + str(total_wrong) + bcolors.ENDC)
