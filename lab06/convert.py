
#def 

#def to_dec_float(value, signs):
    

def to_bin_float(value, signs):
    int_part = int(value)
    float_part = value - int_part
    
    res = []
    while int_part:
        res.append(int_part % 2)
        int_part //= 2
    res.reverse()

    if res == []:
        res.append(0)
    res.append('.')

    pw = 1.0
    for i in range(signs):
        pw /= 2.0
        res.append(1 if float_part > pw - 1e-10 else 0)
        if float_part > pw - 1e-10:
            float_part -= pw

    return res

print(to_bin_float(0.75, 10))
print(to_bin_float(0.25, 10))
print(to_bin_float(0.33, 10))
