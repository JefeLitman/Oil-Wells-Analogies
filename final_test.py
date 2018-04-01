def entry_to_float(self, string):
    parte_entera = ''
    parte_decimal = ''
    flag = False
    for x in string:
        if ((
                x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == '0') and flag == False):
            parte_entera = parte_entera + x
        elif (x == '.'):
            flag = True
        elif ((
                      x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == '0') and flag):
            parte_decimal = parte_decimal + x
    if (parte_decimal == ''):
        return float(int(parte_entera))
    else:
        return int(parte_entera) + (1.0 * int(parte_decimal) / (10 ** len(parte_decimal)))