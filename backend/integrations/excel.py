#import excel stuff

DEFAULT_DATA: list = [
    ('13-11-2023', 'TEST1', '200.21', 'intrare'),
    ('13-11-2023', 'TEST2', '200.21', 'intrare'),
    ('13-11-2023', 'TEST3', '200.21', 'intrare'),
    ('13-11-2023', 'TEST4', '200.21', 'intrare'),
    ('13-11-2023', 'TEST5', '200.21', 'intrare'),
    ('13-11-2023', 'TEST6', '200.21', 'intrare')
]

def __get_data_from_excel(file: str) -> list:
    """
    Get data from an excel file
    """
    import csv

    ret_data = []

    with open(file, 'r', newline='') as fisier:
        cititor = csv.reader(fisier)
        verif = False
        prim = False
        for rand in cititor:
            if rand and len(rand) > 0:
                for el in rand:
                    if el == "Sold contabil":
                        verif = True
                        prim = True
                if verif and not prim:
                    data = "-".join(rand[0].split('-')[::-1])
                    nume = rand[2]
                    intrari_verif = False
                    if rand[4] == '':
                        suma = str(abs(float(rand[5].replace(',', ''))))
                        intrari_verif = True
                    else:
                        suma = str(abs(float(rand[4].replace(',', ''))))
                    suma_str = suma.replace(',', '')
                    tva = float(suma_str)
                    if intrari_verif:
                        ret_data.append([data, nume, tva, 'intrare'])
                    else:
                        ret_data.append([data, nume, tva, 'iesire'])

                if verif and prim:
                    prim = False
    return ret_data
