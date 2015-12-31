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

