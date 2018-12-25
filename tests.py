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
    ('salon lampa prawa załącz', 'on D3'),

    ('Załącz', 'error'),
    ('wyłącz', 'error'),
    ('Załącz światło w kuchni', 'on E7'),
    ('Załącz oświetlenie okapu', 'error'),
    # if this should be toggle E4 or rather error?
    ('Załóż oświetlenie okapu w kuchni', 'toggle E4'),
    ('Wyłącz oświetlenie w kuchni', 'off E7'),
    ('Załącz oświetlenie górne w salonie', 'on D1'),
    ('Załącz lampę lewą w salonie', 'on D2'),
    ('salon lampa prawa Załącz co wy na to', 'on D3'),
    ('Załącz lampę prawą w salonie', 'on D3'),
    ('Wyłącz oświetlenie w salonie', 'off D4'),
    ('Załącz oświetlenie górne w kuchni', 'on E1'),
    ('kuchnia oświetlenie okapu Załącz', 'on E4'),
    ('Załącz wentylator w kuchni', 'on E6'),
    ('Załącz wentylator kuchni', 'on E6'),
    ('Załącz wentylator okapu', 'error'),
    # TODO fix function getting device id
    ('Załącz wentylator okapu w kuchni', 'on E5'),
    ('Załącz okap w kuchni', 'on E5'),
    # todo why it finds HOOD?
    ('Załącz oświetlenie okapu w kuchni', 'on E4'),
    ('kuchnia Załącz oświetlenie pod szafkami', 'on E3'),

    ('Wyłącz całe oświetlenie w kuchni', 'off E7'),
    # todo sometimes it works but not always (function getting type)
    ('Załącz oświetlenie górne w łazience', 'on C1'),
    ('Wyłącz oświetlenie górne w łazience', 'off C1'),
    ('Załącz oświetlenie na suficie w łazience', 'on C1'),
    ('Załącz dmuchawę w łazience', 'on C4'),
    ('Załącz wentylator w łazience', 'on C3'),
    ('Wyłącz wentylator w łazience', 'off C3'),
    ('wentylator w łazience start', 'on C3'),
    ('Załącz oświetlenie górne na poddaszu', 'on A12'),
    ('Wyłącz oświetlenie na poddaszu w sekcji pierwszej', 'off A1'),
    ('on', 'error'),
    ('Wyłącz oświetlenie w sekcji pierwszej Górne na poddaszu', 'off A1'),
    ('Wyłącz całe oświetlenie na poddaszu', 'off A12'),
    ('Załącz monitor', 'error'),
    ('Załącz radio na poddaszu', 'on A3'),
    ('Wyłącz radio na poddaszu', 'off A3'),
    # wrong format (trzeci -> 3)
    ('radio na poddaszu kanał trzeci', 'error'),
    ('radio na poddaszu Kanał 3', 'set A3 ch 3'),
    ('Załącz oświetlenie za telewizorem na poddaszu', 'on A11'),
    ('Załącz oświetlenie za telewizorem na poddaszu w sekcji drugiej', 'on A11'),

    ('Załącz telewizor na poddaszu', 'on A10'),
    ('off', 'error'),
    ('telewizor na poddaszu Kanał 6', 'set A10 ch 6'),
    ('telewizor na poddaszu głośność 7', 'set A10 vol 7'),
    ('Wyłącz całe oświetlenie na poddaszu', 'off A12'),
    ('Załącz oświetlenie górne w sypialni', 'on B1'),
    ('Załącz oświetlenie na suficie w sypialni', 'on B1'),
    ('Ustaw barwa ciepłą oświetlenia górnego w sypialni', 'warm B1'),
    # todo? brak funkcji (trivial function ??)
    ('sypialnia oświetlenie górne barwa zimna', 'cold B1'),
    # todo? nie obsługujemy 'mergowania' - zwracana jest jedna funkcja
    ('Załącz lampę prawą i lewą w sypialni', 'on B3'),
    # the same
    ('Załącz lampy w sypialni', 'on B4'),
    ('Wyłącz całe oświetlenie w sypialni', 'off B7'),
    ('Załącz oświetlenie za telewizorem w sypialni', 'on B6'),
    ('Załącz lampę za telewizorem w sypialni', 'on B6'),
    ('Załącz oświetlenie górne w salonie', 'on D1'),
    # todo change to toggle (trivial function)
    ('lampa lewa w sypialni', 'toggle B2'),
    # color in polish?
    ('salon lampa lewa kolor niebieski', 'set D2 color niebieski'),
    # turn on only one lamp
    ('lampa lewa w sypialni kolor czerwonysypialnia lampa prawa kolor czerwo', 'set B2 color czerwony'),
    ('Załącz budzik w sypialni', 'on B8'),
    # lack of function
    ('budzik w sypialni godzina 6:00 rano', 'error'),

    # todo brak funkcji! you can enter something like trivial function
    ('budzik w sypialni 6:00', 'error'),
    ('budzik w sypialni godzina 0600', 'error'),
    ('budzik w sypialni godzina 13:00', 'error'),
    ('budzik w sypialni budzenie 6:00', 'error'),
    ('budzik w sypialni ustaw 7:00', 'set B8 time 7:00'),
    ('budzik w sypialni 20:00', 'error'),
    ('salon roleta lewa dół', 'down D5'),
    ('salon roleta lewa stop', 'stop D5'),
    ('roleta lewa w górę', 'error'),
    ('Zatrzymaj roletę lewą w sypialni', 'error'),
    ('Zasłoń rolety w sypialni', 'error'),
    ('roleta prawa w sypialni w górę', 'error'),
    ('roleta lewa w salonie w dół', 'down D5'),
    ('rolety w sypialni w górę', 'error'),
    ('rolety w salonie w górę', 'up D7'),
    ('Opuść zasłony w sypialni w salonie dobra to jeszcze raz kasujemy', 'error'),
    ('Opuść rolety w salonie', 'down D7'),
    ('w salonie w górę', 'error'),
    ('rolety w salonie w górę', 'up D7'),
    ('rolety w salonie w dół', 'down D7'),
    ('Zatrzymaj rolety w salonie', 'stop D7')

]

formal_language = yaml.load(open('V_4.yaml'))

total_correct = total_wrong = 0
for (command, expected) in test_cases:
    result = None
    try:
        result = parse_command(command, formal_language)
    except:
        total_wrong += 1
    if expected != result:
        print('result = ' + str(result) + ' | expected = ' + expected)
        total_wrong += 1
    else:
        print('result = expected = ' + expected)
        total_correct += 1

print('\n')
print('total = ' + str(len(test_cases)))
print('total correct = ' + str(total_correct))
print('total wrong = ' + str(total_wrong))

