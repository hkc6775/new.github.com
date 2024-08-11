import phonenumbers

def traitementEmail(email):
    tab = ["=", '/', '>', '<', '!', '%', '*', '+',
           ")", "("]
    i = 0
    if email:
        for i in tab:
            if i in email:
                return False
    return True

def traitementTel(tel):
    try:
        if tel[:2] == "07" or tel[:2] == "05" or tel[:2] == "01":
            if len(tel[2:]) == 8:
                for x in tel[2:]:
                    x = int(x)
                    if x >= 0 or x <= 9:
                        return True
    except Exception as e:
            return False