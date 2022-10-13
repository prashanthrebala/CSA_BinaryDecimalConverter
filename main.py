okgr = '\033[96m'
endc = '\033[0m'


# 60 bits of floating point precision
def decimal_to_binary(x, precision=60):
    x = str(x)
    whole, fraction = x.split(".")
    bin_whole = bin(int(whole))
    fraction = float(f"0.{fraction}")
    bin_fraction = "."
    for i in range(precision):
        if 2 ** ~i <= fraction:
            bin_fraction += "1"
            fraction -= 2 ** ~i
        else:
            bin_fraction += "0"
    return bin_whole + bin_fraction


def binary_to_decimal(x):
    whole, fraction = x.split(".")
    whole = int(whole, 2)
    fraction_dec = 0
    for i in range(len(fraction)):
        if fraction[i] == '1':
            fraction_dec += 2 ** ~i
    return whole + fraction_dec


def single_precision(value):
    # 1 sign-bit, 8 exp bits, 23 mantissa bits
    # index of '.' - index of '1' - 1
    sign = '1' if value[0] == '-' else '0'
    exp = value.index('.') - value.index('1') - 1
    if exp < 0:
        exp += 1
    exp = 127 + exp
    _8 = '{:08b}'.format(exp & 0xff)
    mantissa = ""
    index = value.index('1') + 1
    while len(mantissa) < 23:
        if value[index] != '.':
            mantissa += value[index]
        index += 1
    return {
        "sign": sign,
        "exponent": _8,
        "mantissa": mantissa,
        "binary": spaces(sign + _8 + mantissa)
    }


def double_precision(value):
    # 1 sign-bit, 11 exp bits, 52 mantissa bits
    # index of '.' - index of '1' - 1
    sign = '1' if value[0] == '-' else '0'
    exp = value.index('.') - value.index('1') - 1
    if exp < 0:
        exp += 1
    exp = 1023 + exp
    _11 = '{:011b}'.format(exp & 0x7ff)
    mantissa = ""
    index = value.index('1') + 1
    while len(mantissa) < 52:
        if value[index] != '.':
            mantissa += value[index]
        index += 1
    return {
        "sign": sign,
        "exponent": _11,
        "mantissa": mantissa,
        "binary": spaces(sign + _11 + mantissa)
    }


def get_binary(a):
    _32 = '{:032b}'.format(a & 0xffffffff)
    _64 = '{:064b}'.format(a & 0xffffffffffffffff)
    return {
        "32bit": spaces(_32),
        "64bit": spaces(_64)
    }


def get_hex(a):
    _32 = '{:08x}'.format(a & 0xffffffff)
    _64 = '{:016x}'.format(a & 0xffffffffffffffff)
    return {
        "32bit": spaces(_32),
        "64bit": spaces(_64)
    }


def converter():
    floating_point = False
    while True:
        color = '\033[0m'
        print(f"\n{okgr}Press 'f' to toggle b/w floating and integer {endc}")
        try:
            if floating_point:
                inp = input("waiting for floating point input...\n")
                if inp[0].lower() == 'f':
                    floating_point = False
                    continue
                if inp[0] == 'b':
                    print_floats(binary_to_decimal(inp[1:]))
                else:
                    print_floats(inp)
            else:
                inp = input("waiting for input... \nprefix with 'b' for binary, 'x' for hex:\n")
                inp = inp.replace(" ", "")
                if inp[0].lower() == 'f':
                    floating_point = True
                    continue
                if len(inp) > 0:
                    if inp[0] == 'b':
                        x = int(inp[1:], 2)
                    elif inp[0] == 'x':
                        x = int(inp[1:], 16)
                    else:
                        x = int(inp)
                    print_whole_values(x)
        except Exception as e:
            print(e)


def print_floats(x):
    print("Decimal: ", x)
    f = decimal_to_binary(x)
    print("Binary: ", f)
    sp = single_precision(f)
    print(f"SinglePrecision: {sp['sign']} {sp['exponent']} {sp['mantissa']}")
    print(f"SP Binary: {sp['binary']}")
    print(f"SP HexDec: {hex(int(sp['binary'].replace(' ', ''), 2))}")
    dp = double_precision(f)
    print(f"DoublePrecision: {dp['sign']} {dp['exponent']} {dp['mantissa']}")
    print(f"DP Binary: {dp['binary']}")
    print(f"DP HexDec: {hex(int(dp['binary'].replace(' ', ''), 2))}")


def print_whole_values(x):
    bn = get_binary(x)
    hx = get_hex(x)
    print("Decimal: ", x)
    print("32b Binary: ", bn["32bit"])
    print("64b Binary: ", bn["64bit"])
    print("32b HexDec: ", hx["32bit"])
    print("64b HexDec: ", hx["64bit"])
    print()


def spaces(string, x=4):
    return " ".join([string[i: i + x] for i in range(0, len(string), x)])


if __name__ == '__main__':
    converter()

