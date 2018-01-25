from Sem_Op import *

class Analyse_Erreur(Exception):pass



namefile = input("donner un nom de fichier :")

f = open(namefile, 'r')
lignes = []

current_line = f.readline()
while current_line != "":
      lignes = lignes + [current_line]
      print(current_line)
      current_line = f.readline()

f.close()

print(lignes)


def clear_comments(lg):
      if lg == []:
            return []
      elif lg[0] == []:
            return clear_comments(lg[1:])
      elif lg[0][0] == '#':
            return clear_comments(lg[1:])
      elif lg[0][0] in [' ','\t'] :
            return clear_comments([lg[0][1:]] + lg[1:])
      else:
            return [lg[0]] + clear_comments(lg[1:])

lignes_no_comments = clear_comments(lignes)                                  
print("sans commentaires",lignes_no_comments)

def remove(l,e):
      if l == []:
            return l
      elif l[0] == e:
            return remove(l[1:],e)
      else:
            return [l[0]] + remove(l[1:],e)

def separate_words(lg):
      lw = []
      for line in lg:
            lwi = line.rstrip('\n\r\t').split(" ")
            lw = lw + remove(remove(lwi,' '),'')
      return lw

liste_words = separate_words(lignes_no_comments)

print("words ",liste_words)

def opposite(ch):
      if ch =='(':
            return ')'
      elif ch == '{':
            return '}'
      elif ch == ')':
            return '('
      elif ch == '}':
            return '{'
      else:
            return "not a bracket"

def ouvrantes(ch):
      return ch in ['(','{']

def fermantes(ch):
      return ch in [')','}']

def well_formed(lw):
      pile = []
      for w in lw:
            if ouvrantes(w):
                  pile = [w] + pile
            elif fermantes(w):
                  if pile == []:
                        return False
                  elif w == opposite(pile[0]):
                        pile = pile[1:]
                  else:
                        return False
      return pile == []

print("well_formed",well_formed(liste_words))

                        
      
motscles = ['if','then','do','while','else',':=','=','<=','not','neg','and','or','true','false','bool']

def identifier(wd):
      return wd.isalpha() and not (wd in motscles)

def nombre(wd):
      try:
            return int(wd)
      except ValueError:
            return wd
      



def analyse_arith(lw,cur_ind,fin,prev_struct,expected):
      #print('analyse arith : cur_ind',cur_ind,' prev_struc ',prev_struct,' exp ',expected)
      if cur_ind == fin :
            raise Analyse_Erreur
      elif type(nombre(lw[cur_ind])) == int:
            #print('un nombre')
            arbre_nb = {'int' : nombre(lw[cur_ind])}
            if expected == []:
                  return (cur_ind+1,arbre_nb)
            else:
                  return analyse_arith(lw,cur_ind+1,fin,[arbre_nb]+prev_struct,expected)
      elif identifier(lw[cur_ind]):
            #print('un identificateur')
            arbre_id = {'var' : lw[cur_ind]}
            if expected == []:
                  return (cur_ind+1,arbre_id)
            else:
                  return analyse_arith(lw,cur_ind+1,fin,[arbre_id]+prev_struct,expected)
      elif lw[cur_ind] == '(':
            #print('parenthese ( et expected ',expected)
            return analyse_arith(lw,cur_ind+1,fin,prev_struct,[')']+expected)            
      elif lw[cur_ind] == ')':
            #print('parenthese )')
            if expected == []:
                  print('erreur )')
                  raise Analyse_Erreur
            elif expected[0] == ')':
                  if len(expected) == 1:
                        return (cur_ind+1,prev_struct[0])
                  else:
                        return analyse_arith(lw,cur_ind+1,fin,prev_struct,expected[1:])
            else:
                  raise Analyse_Erreur
      elif lw[cur_ind] in ['+','-','*']:
            #print('op bin ',lw[cur_ind],'prev ',prev_struct,'expected ',expected)
            if prev_struct == []:
                  raise Analyse_Erreur
            else:
                  arbre_g = prev_struct[0]
                  (next_ind,arbre_d)=analyse_arith(lw,cur_ind+1,fin,[],[])
                  arbre_op = {'op' : lw[cur_ind], 'g' : arbre_g, 'd' : arbre_d}
                  if expected == []:
                        return (next_ind,arbre_op)
                  else:
                        return analyse_arith(lw,next_ind,fin,[arbre_op]+prev_struct[1:],expected)
      else:
            raise Analyse_Erreur
"""
print('NEW ONE 1')

liste_arith1 = [ '(', '2', '+', '(', 'x','*','3',')',')']

try:
      print(len(liste_arith1),analyse_arith(liste_arith1,0,len(liste_arith1),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW ONE 2')

liste_arith2 = [ '(', '(','2', '+', '4',')','+','(', 'x','*','3',')',')']                  
                  
try:
      print(len(liste_arith2),analyse_arith(liste_arith2,0,len(liste_arith2),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW ONE 3')

liste_arith3 = [ '(', '(','2', '+', '4',')','+','(', 'x','*','3',')',')','+','2']                  
                  
try:
      print(len(liste_arith3),analyse_arith(liste_arith3,0,len(liste_arith3),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW ONE 4')

liste_arith4 = [ '(', '(','2', '+', '4',')','+','(', 'x','*','3',')',')','3']                  
                  
try:
      print(len(liste_arith4),analyse_arith(liste_arith4,0,len(liste_arith4),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW ONE 5')

liste_arith5 = [ '2', '+', '4']                  
                  
try:
      print(len(liste_arith5),analyse_arith(liste_arith5,0,len(liste_arith5),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')
            
print('NEW ONE 6')

liste_arith6 = [ '(','2', '+', '4',')']                  
                  
try:
      print(len(liste_arith6),analyse_arith(liste_arith6,0,len(liste_arith6),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')
"""

def analyse_bool(lw,cur_ind,fin,prev_struct,expected):
      #print('analyse_bool cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
      try:
            (next_ind,arbre_exp) = analyse_arith(lw,cur_ind,fin,[],[])
            return analyse_bool(lw,next_ind,fin,[arbre_exp]+prev_struct,expected)
      except Analyse_Erreur:
            if cur_ind == fin :
                  raise Analyse_Erreur
            elif lw[cur_ind] in ['true','false']:
                  #print(' true false cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
                  arbre_bo = {'bool' : lw[cur_ind]}
                  if expected == []:
                        return (cur_ind+1,{'bool' : lw[cur_ind]})
                  else:
                        return analyse_bool(lw,cur_ind+1,fin,[arbre_bo]+prev_struct,expected)
            elif lw[cur_ind] == 'neg':
                  #print(' neg cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
                  (next_ind,arbre_neg) = analyse_bool(lw,cur_ind+1,fin,prev_struct,expected)
                  if expected == []:
                        return (next_ind, { 'neg' : arbre_neg })
                  else:
                        return analyse_bool(lw,cur_ind+1,fin, [{ 'neg' : arbre_neg }]+prev_struct,expected)
            elif lw[cur_ind] == '(':
                  #print(' ( cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
                  return analyse_bool(lw,cur_ind+1,fin,prev_struct,[')']+expected)
            elif lw[cur_ind] == ')':
                  #print('ici ) cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
                  if expected == [] or prev_struct == []:
                        # print('erreur )')
                        raise Analyse_Erreur
                  elif len(expected) == 1:
                        return (cur_ind+1,prev_struct[0])
                  else:
                        # print('verif len(lw)',len(lw),' cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
                        return analyse_bool(lw,cur_ind+1,fin,prev_struct,expected[1:])    
            elif lw[cur_ind] in ['=','<=']:
                  print(' = <= cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
                  if prev_struct == []:
                        raise Analyse_Erreur
                  else:
                        arbre_g = prev_struct[0]
                        if isexparith(arbre_g):
                              # print(' appel a analyse_arith')
                              (next_ind,arbre_d)=analyse_arith(lw,cur_ind+1,fin,prev_struct[1:],[])
                              arbre_opbin = {'comp' : lw[cur_ind], 'g' : arbre_g, 'd' : arbre_d}
                              if expected == []:
                                    return (next_ind,arbre_opbin)
                              else:
                                    return analyse_bool(lw,next_ind,fin,[arbre_opbin]+prev_struct[1:],expected)
                        else:
                              raise Analyse_Erreur
            elif lw[cur_ind] in ['or','and']:
                  print(' or and cur_ind ',cur_ind,' prev_struct ',prev_struct,' expected ',expected)
                  if prev_struct == []:
                        raise Analyse_Erreur
                  else:
                        arbre_g = prev_struct[0]
                        if isexpbool(arbre_g):
                              # print('isexpbool')
                              (next_ind,arbre_d)=analyse_bool(lw,cur_ind+1,fin,prev_struct[1:],[])
                              arbre_opbin= {'opbin' : lw[cur_ind], 'arg1' : arbre_g, 'arg2' : arbre_d}
                              if expected ==[]:
                                    return (next_ind,arbre_opbin)
                              else:
                                    return analyse_bool(lw,next_ind,fin,[arbre_opbin]+prev_struct[1:],expected)
                        else:
                              # print('bizarre on est ici')
                              raise Analyse_Erreur
            else:
                  raise Analyse_Erreur
 

print('NEW TWO 0')

liste_bool =['neg', '(', 'i', '=', '(', 'x', '+', '1',')', ')']

print('liste_bool',liste_bool)

try:
      analyse_arith(liste_bool,4,len(liste_bool),[],[])
      print('succ analyse arithmetique ( x + 1 ) :',liste_bool,' wait 9 :')
except Analyse_Erreur:
      print('echec analyse arith')
      
try:
      print(len(liste_bool),analyse_bool(liste_bool,0,len(liste_bool),[],[]))
      print('succ analyse booléenne ')
except Analyse_Erreur:
      print('echec analyse_erreur')

""""
print('NEW TWO 1')

liste_bool1 = [ 'neg', '(','a', '=', 'b',')']

try:
      print(len(liste_bool1),analyse_bool(liste_bool1,0,len(liste_bool1),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW TWO 2')

liste_bool2 = [ '(', '(','2', '+', '4',')','<=','(', 'x','*','3',')',')']                  
                  
try:
      print(len(liste_bool2),analyse_bool(liste_bool2,0,len(liste_bool2),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW TWO 3')

liste_bool3 = [ '(', '(','2', '=', '4',')','or','(', 'x','<=','3',')',')']                  
                  
try:
      print(len(liste_bool3),analyse_bool(liste_bool3,0,len(liste_bool3),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW TWO 4')

liste_bool4 = [ '(', '(','2', '=', '4',')','or','neg','(', 'x','<=','3',')',')']  

                  
try:
      print(len(liste_bool4),analyse_bool(liste_bool4,0,len(liste_bool4),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')

print('NEW TWO 5')

liste_bool5 = [ '(', '(','2', '=', '4',')','or','neg','neg','(', 'x','<=','3',')',')'] 
                
                  
try:
      print(len(liste_bool5),analyse_bool(liste_bool5,0,len(liste_bool5),[],[]))
except Analyse_Erreur:
      print('echec analyse_erreur')
            
"""     

def analyse_prog(lw,cur_ind,fin,prev_struct,expected):
      #print("analyse prog cur_ind ",cur_ind,"word ",lw[cur_ind]," prev_struct ",prev_struct," expected ",expected)
      if cur_ind == fin :
            print("détection anormale de fin de fichier")
            raise Analyse_Erreur
      elif lw[cur_ind] == 'skip':
            if expected ==[]:
                  return (cur_ind+1,{'skip' :'_'})
            else:
                  return analyse_prog(lw,cur_ind+1,fin,[{'skip' :'_'}]+prev_struct,expected)
      elif lw[cur_ind] == ';':
            if prev_struct == []:
                  raise Analyse_Erreur
            else:
                  (next_ind,arbre_seq) = analyse_prog(lw,cur_ind+1,fin,[],[])
                  arbre_seq = {'c1' : prev_struct[0],'c2' : arbre_seq}
                  if expected == []:
                        print("; prev_struct",prev_struct," expected ",expected)
                        return (next_ind,arbre_seq)
                  else:
                        print("; prev_struct",prev_struct," expected ",expected)
                        return analyse_prog(lw,next_ind,fin,[arbre_seq]+prev_struct[1:],expected)
      elif lw[cur_ind] =='{':
            #print(' trouver { ')
            return analyse_prog(lw,cur_ind+1,fin,prev_struct,['}']+expected)
      elif lw[cur_ind] == '}':
            if expected == []:
                  raise Analyse_Erreur
            elif expected == ['}']:
                  print("{ prev_struct",prev_struct," expected ",expected)
                  return (cur_ind+1, prev_struct[0])
            else:
                  print("{ prev_struct",prev_struct," expected ",expected)
                  return analyse_prog(lw,cur_ind+1,fin,prev_struct,expected[1:])
      elif identifier(lw[cur_ind]):
            #print("trouver un identifieur ",cur_ind,'',lw[cur_ind])
            if lw[cur_ind+1]== ':=':
                  print("trouver affectation :=")
                  (next_ind,arbre_exp) = analyse_arith(lw,cur_ind+2,fin,[],[])
                  arbre_assign = {'var' : lw[cur_ind], 'exp' : arbre_exp}
                  print(arbre_assign)
                  if expected == []:
                        print("identifier prev_struct",prev_struct," expected ",expected)
                        return (next_ind,arbre_assign)
                  else:
                        print("identifier prev_struct",prev_struct," expected ",expected)
                        return analyse_prog(lw,next_ind,fin,[arbre_assign]+prev_struct,expected)
            else:
                  Erreur_Analyse
      elif lw[cur_ind] == 'while':
            print("prev_struct a l'appel du while",prev_struct," expected ",expected)
            (ind_cond,arbre_cond)=analyse_bool(lw,cur_ind+1,fin,[],[])
            print("cond while trouvee",arbre_cond)
            if lw[ind_cond] == 'do':
                  print("début corps de boucle ",lw[ind_cond+1])
                  (ind_do,arbre_do)= analyse_prog(lw,(ind_cond+1),fin,[],[])
                  print("arbre corps boucle ",arbre_do)
                  arbre_while = {'whiledo' : arbre_do, 'cond' : arbre_cond}
                  print("expected ",expected)
                  if expected==[]:
                        print("while fin de fichier")
                        return (ind_do,arbre_while)
                  else:
                        return analyse_prog(lw,ind_do,fin,[arbre_while]+prev_struct,expected)
            else:
                  raise Analyse_Erreur            
      elif lw[cur_ind] == 'if':
            (ind_cond,arbre_cond)=analyse_bool(lw,cur_ind+1,fin,[],[])
            #print(' arbre cond ',arbre_cond)
            if lw[ind_cond] == 'then':
                  (ind_then,arbre_then)=analyse_prog(lw,(ind_cond+1),fin,[],[])
                  print('arbre then ',arbre_then)
            else:
                  raise Analyse_Erreur
            #print("on commence le else")
            if lw[ind_then] == 'else':
                  #print("trouver le else a l'indice ", ind_then)
                  (ind_else,arbre_else)=analyse_prog(lw,(ind_then+1),fin,[],[])
                  #print('arbre else ',arbre_else)
            if expected == []:
                  return (ind_else,{'cond' : arbre_cond, 'then' : arbre_then, 'else' : arbre_else})
            else:
                  arbre_if = {'cond' : arbre_cond, 'then' : arbre_then, 'else' : arbre_else}
                  return analyse_prog(lw,ind_else+1,fin,[arbre_if]+prev_struct,expected)
      else:
            raise Analyse_Erreur
      
print("analyse prog :",liste_words)

result = analyse_prog(['{']+liste_words+['}'],0,len(liste_words)+2,[],[])
                        
print('l arbre résultant est :',result)

print("est programe ", isprog(result[1]))

print("evaluation ",evalprog(result[1],{}))
      
