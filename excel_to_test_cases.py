import pandas as pd
import os

COMMAND = 'Tekst polecenia'
EXPECTED = 'oczekiwana komenda'
ALTERNATIVE = 'alternatyna komenda'
NAN = 'nan'

if __name__ == "__main__":
    if not os.path.exists('output'):
        os.makedirs('output')

    input_file = r'data/dane-testowe.xls'
    output_file = r'output/test_cases.txt'
    df = pd.read_excel(input_file, sheet_name="dane")

    with open(output_file, 'w') as file:
        for nr, row in df.iterrows():
            if ALTERNATIVE in row and str(row[ALTERNATIVE]) != NAN:
                file.write('(\'' + row[COMMAND] + '\', (\'' + row[EXPECTED] + '\', \'' +
                           str(row[ALTERNATIVE]) + '\')),\n')
            else:
                file.write('(\'' + row[COMMAND] + '\', (\'' + row[EXPECTED] + '\')),\n')
