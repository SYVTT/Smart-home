import yaml

from wdsjn_function import parse_command

test_cases = [
    ('zapal światło na poddaszu w sekcji pierwszej', 'on A1'),
    ('załącz oświetlenie na poddaszu', 'on A12'),
    ('włącz komputer na poddaszu', 'on A4'),
    ('w sypialni lewą lampę załącz', 'on B2'),
    ('toaleta uruchom wentylator', 'on C3'),
    ('zgaś światło w salonie', 'off D4'),
    ('wyłącz wentlator w kuchni', 'off E6'),
    ('włącz całe oświetlenie w kuchni', 'on E7'),
    ('ustaw budzik w sypialni na 13:00', 'set B8 time 13:00'),
    ('ustaw kanał TV w sypialni na 16', 'set B5 ch 16'),
    ('salon lampa prawa załącz', 'on D3')
]

formal_language = yaml.load(open('V_4.yaml'))

for (command, expected) in test_cases:
    result = None
    try:
        result = parse_command(command, formal_language)
    except:
        pass
    if expected != result:
        print('result = ' + str(result) + ' | expected = ' + expected)
    else:
        print('result = expected = ' + expected)
