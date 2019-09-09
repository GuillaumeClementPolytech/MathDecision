# Return the number of possible groups for n person
# données: n : Int : nombre d'eleves
# Resultat : [Int, Int] Nombre minimum et maximum de groupes (de 2 ou 3 personnes)
def nombres_possibles_groupes(n):
    if n <= 1:
        return [0, 0]
    elif n % 6 == 0:
        return [n / 2, n / 3]
    elif n % 2 != 0:
        tmp = nombres_possibles_groupes(n - 3)
        tmp[1] = tmp[1] + 1
        tmp[0] = tmp[0] + 1
        return tmp
    else:
        tmp = nombres_possibles_groupes(n - 2)
        tmp[1] = tmp[1] + 1
        tmp[0] = tmp[0] + 1
        return tmp


#Données: nb_eleves  : nombre d'eleves
#         nb_groupes : nombre de groupes a former (de 2 ou 3 eleves)
#Le nb_groupes doit etre entre le minimum et le maximum de nombre_groupes(nb_eleves)
#Resultat : [Int, Int] : Nombre de groupes de 2 et de groupes de 3 respectivement
def repartition_nombre_groupes(nb_eleves,nb_groupes):
    if nb_eleves % 2 == 0:
        res = [nb_eleves / 2, 0]
        while res[0] + res[1] > nb_groupes:
            res[0] = res[0] - 3
            res[1] = res[1] + 2
        return res
    else:
        tmp =  repartition_nombre_groupes(nb_eleves - 3 , nb_groupes - 1)
        tmp[1] = tmp[1] + 1
        return tmp

#Donnees: nbr_grps_2 : nombre de groupes de 2 eleves
#         nbr_grps_3 : nombre de groupes de 3 eleves
#Resultat : Int, nombre d'enumerations de (nbr_grps_2 + nbr_grps_3) eleves dans nbr_grps_2 groupes de 2 et nbr_grps_3 groupes de 3
def compter_enumerations_fixe(nbr_grps_2, nbr_grps_3):
    if nbr_grps_2 <= 1 and nbr_grps_3 <= 0:
        return 1
    elif nbr_grps_2 <= 0 and nbr_grps_3 <= 1:
        return 1
    nb_eleves = (nbr_grps_2 * 2 + nbr_grps_3 * 3)
    if nbr_grps_2 > 0 and nbr_grps_3 > 0:
        small = ( ( nb_eleves - 1) * compter_enumerations_fixe(nbr_grps_2 - 1, nbr_grps_3))
        big = ((( nb_eleves - 1) * ( nb_eleves - 2 )/ 2) * compter_enumerations_fixe(nbr_grps_2 , nbr_grps_3 - 1))
        return small + big
    elif nbr_grps_2 > 0:
        return ( ( nb_eleves - 1) * compter_enumerations_fixe(nbr_grps_2 - 1, nbr_grps_3))
    else :
        return ( ( ( nb_eleves - 1) * ( nb_eleves - 2 )/ 2) * compter_enumerations_fixe(nbr_grps_2 , nbr_grps_3 - 1))


def compter_enumerations(nb_eleves):
    nbr_grps_possibles = nombres_possibles_groupes(nb_eleves)
    nbr_grps_max = nbr_grps_possibles[0]
    nbr_grps_min = nbr_grps_possibles[1]
    repartition = repartition_nombre_groupes(nb_eleves, nbr_grps_max)
    nbr_grps = repartition[0] + repartition[1]
    sum = 0
    while nbr_grps >= nbr_grps_min:
        sum = sum + compter_enumerations_fixe(repartition[0] , repartition[1])
        repartition[0] = repartition[0] - 3
        repartition[1] = repartition[1] + 2
        nbr_grps = repartition[0] + repartition[1]
    return sum

#
def enumerations_fixes(set_eleves, repartition):
    set_temp = set_eleves.copy()
    if repartition[0] <= 1 and repartition[1] <= 0:
        return [[[set_temp.pop(), set_temp.pop()]]]
    elif repartition[0] <= 0 and repartition[1] <= 1:
        return [[[set_temp.pop(), set_temp.pop(), set_temp.pop()]]]
    eleve = set_temp.pop()
    res = []
    if repartition[0] > 0:
        for eleve2 in set_temp:
            set_temp2 = set_temp.copy()
            set_temp2.discard(eleve2)
            res_temp = enumerations_fixes(set_temp2, [repartition[0] - 1, repartition[1]])
            for i in range(0, len(res_temp)):
                res_temp[i].append([eleve, eleve2])
            res.extend(res_temp)
    if repartition[1] > 0:
        for eleve2 in set_temp:
            set_temp2 = set_temp.copy()
            set_temp2.discard(eleve2)
            for eleve3 in set_temp2:
                if eleve2 < eleve3:
                    set_temp3 = set_temp2.copy()
                    set_temp3.discard(eleve3)
                    res_temp = enumerations_fixes(set_temp3, [repartition[0], repartition[1] - 1])
                    for i in range(0, len(res_temp)):
                        res_temp[i].append([eleve, eleve2, eleve3])
                    res.extend(res_temp)
    return res


# Prends un set d'eleves, renvoie un tableau de tableaux de tableaux (un tableau de tableaux == une enumeration)
#
def enumerations(set_eleves):
    if len(set_eleves) < 2:
        return []
    else:
        nbr_grps_possibles = nombres_possibles_groupes(len(set_eleves))
        nbr_grps_max = nbr_grps_possibles[0]
        nbr_grps_min = nbr_grps_possibles[1]
        repartition = repartition_nombre_groupes(len(set_eleves), nbr_grps_max)
        nbr_grps = repartition[0] + repartition[1]
        res = []
        while nbr_grps >= nbr_grps_min:
            res.extend(enumerations_fixes(set_eleves, repartition))
            repartition[0] = repartition[0] - 3
            repartition[1] = repartition[1] + 2
            nbr_grps = repartition[0] + repartition[1]
        return res


print(nombres_possibles_groupes(100))
res = repartition_nombre_groupes(100,34)
print(res)
print(res[0] * 2 + res[1] * 3)
res = repartition_nombre_groupes(100,50)
print(res)
print(res[0] * 2 + res[1] * 3)

for i in range(2,12):
    print("Enumeration de "+ str(i) +" eleves : "+ str(compter_enumerations(i)) +" groupages possibles.")

b = {"e1","e2","e3","e4","e5","e6"}



print(b)
print("------")
res = enumerations(b)
for enum in res:
    print(enum)
print("------")
print(len(res))
print(b)
