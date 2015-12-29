import re

# FIRST PRIORITY
street = ['ul', 'pl', 'ulic', 'plac']

# SECOND PRIORITY LOCATIONS
place = ['park',]

# THIRD PRIORITY LOCATIONS
district = ['dzielnic',]


def match_words(data):
    """Looks for location names in provided string"""
    pattern = r'((?:{})[aemuy]{{0,2}})[\. ]+(\w+(?:\s[A-Z]\w+)?)'.format('|'.join(street))
    scrap = re.findall(pattern, data)
    return [' '.join(address) for address in scrap]


if __name__ == '__main__':
    debug_sentence = """Do wynajęcia duży pokój w centrum miasta. Mieszkanie mieści się obok Rynku, przy ulicy Igielnej. W mieszkaniu znajdują się jeszcze 2 pokoje zamieszkiwane przez 2 osoby. Koszt wynajęcia pokoju to 490 złotych od osoby (w tym opłaty, bez internetu). Zapraszamy do oglądania!:) """
    result = match_words(debug_sentence)
    print(result)
    # with open('words.txt', 'w') as writer:
    #     writer.write(str(result))
