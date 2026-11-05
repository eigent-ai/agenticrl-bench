def SuperScriptinate(number_str):
    superscripts = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
    return number_str.translate(superscripts)


def sci_notation(number, sig_fig=2):
    ret_str = "{:.{prec}e}".format(number, prec=sig_fig)
    a, b = ret_str.split("e")
    b = int(b)
    return a + "x10^" + SuperScriptinate(str(b))
