# -*- coding: utf8 -*-

"""Tables d'association implementees par adressage direct      """



class InvalidKey(Exception):pass


def emptyAssoc():
    """
    emptyAssoc : --> Assoc
    constante correspondant a la table d'association vide
    """
    return {}



def search(k,t):
    """
    search: key -->elem
    search(k,t) cherche dans la table t et renvoie l'element d'information indexe par la cle k
    Si k n'est pas de type str ou t n'a pas de cle k, l'exception InvalidKey est levee.
    """
    if not(type(k)==str):
        raise InvalidKey
    elif not (k in t.keys()):
        raise InvalidKey
    else:
        return t[k]
    


def insert(e,k,t):
    """
    insert: elem x key x Assoc --> Assoc
    insert(e,k,t) ajoute une nouvelle association entre k et e dans la table t
    (la precedente association, si elle existe, est alors perdue)
    """
    if not(type(k)==str):
        raise InvalidKey
    else:
        t[k]=e
        return t


def delete(k,t):
    """
    delete: key x Assoc --> Assoc
    delete(k,t) supprime l'association entre k et e dans la table t
    """
    if not(type(k)==str):
        raise InvalidKey
    if not (k in t.keys()):
        raise InvalidKey
    else:
        del t[k]
        return t
    
 
        
def isEmptyAssoc(t):
    """
    isEmpty: Assoc -->bool
    isEmpty(t) : teste si la table t est vide.
    """
    return t=={}


def printAssoc(t):
    """
    printAssoc : Assoc -->None
    printAssoc(t) : affiche le contenu de la table t sous la forme clé : valeur ligne par ligne
    """
    if isEmptyAssoc(t):
        print("Table Vide")
    else:
        print("Table cle : valeur")
        for i in t.keys():
            print(i,":",t[i])


    
def main():
    a=emptyAssoc()
    a = insert(1,'x',a)
    printAssoc(a)
    a = insert(2,'y',a)
    a = insert(2,'z',a)
    printAssoc(a)
    print("search ('x',a) vaut :",search('x',a))
    a = delete('x',a)
    printAssoc(a)




if __name__ == "__main__" :
    main()
