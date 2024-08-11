def encoder(chaine):
    clef = 3
    message = [(ord(i)+clef) for i in chaine]
    message_decoder = [chr(i) for i in message]
    final = "".join(message_decoder)
    
    return final


def decoder(chaine):
    clef = 3
    message = [(ord(i)-clef) for i in chaine]
    message_decoder = [chr(i) for i in message]
    final = "".join(message_decoder)
    
    return final