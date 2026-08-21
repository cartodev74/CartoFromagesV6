
##fonction pour arrondir un chiffre et mettre un séparateur de milliers
def separateur_millier(num):
    num = round(num)
    return '{:,}'.format(num).replace(',', ' ')