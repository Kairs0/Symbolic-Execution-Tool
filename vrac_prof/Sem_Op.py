from Assoc_Var import *

class Erreur_Evaluation(Exception):pass

motscles = ['if','then','else','while','do','skip']

operators = ['+','-','*']

def isvar(exp):
  return type(exp) == str and not (exp in motscles)

def isoperator(exp):
  return exp in operators
  
def isexparith(exp):
  if type(exp) != dict:
    return False
  else:
    if sorted(exp.keys()) == ['var']:
      return isvar(exp['var'])
    elif sorted(exp.keys()) == ['int']:
      return type(exp['int']) == int
    elif sorted(exp.keys()) == ['d','g','op']:
      return isexparith(exp['g']) and isexparith(exp['d']) and isoperator(exp['op'])
    
def isexpbool(exp):
  if type(exp) !=dict:
    return False
  else:
    if sorted(exp.keys()) == ['bool']:
      return (exp['bool'] in ['true','false'])
    elif sorted(exp.keys()) == ['comp','d','g']:
      return (exp['comp'] in ['=','<=']) and isexparith(exp['g']) and isexparith(exp['d'])
    elif sorted(exp.keys()) == ['neg']:
      return isexpbool(exp['neg'])
    elif sorted(exp.keys()) ==['arg1','arg2','opbin']:
      return (exp['opbin'] in ['or','and']) and isexpbool(exp['arg1']) and isexpbool(exp['arg2'])
    else:
      return False


def isprog(exp):
  if type(exp) !=dict:
    return False
  else:
    if sorted(exp.keys()) == ['skip']:
      return True
    elif sorted(exp.keys()) == ['exp','var']:
      return isvar(exp['var']) and isexparith(exp['exp'])
    elif sorted(exp.keys()) == ['c1','c2']:
      return isprog(exp['c1']) and isprog(exp['c2'])
    elif sorted(exp.keys()) == ['cond','else','then']:
      return isexpbool(exp['cond']) and isprog(exp['then']) and isprog(exp['else'])
    elif sorted(exp.keys()) == ['cond','whiledo']:
      return isexpbool(exp['cond']) and isprog(exp['whiledo'])
    else:
      return False
    

prog = {'c1' : {'var' : 'x', 'exp' : {'int' : 5}},
        'c2' : { 'c1' : {'var' : 'y', 'exp' : {'int' : 15}},
                 'c2' : {'cond' : {'neg' : {'comp' : '=',
                                               'd' : {'var' : 'x'},
                                               'g' : {'var' : 'y'}}},
                         'whiledo' : {'cond' : {'neg' : {'comp' : '<=',
                                                            'g' : {'var' : 'x'},
                                                            'd' : {'var' : 'y'}}},
                                      'then' : {'var':'x',
                                                'exp': {'op':'-',
                                                        'g':{'var':'x'},
                                                        'd':{'var':'y'}}},
                                      'else' : {'var':'y',
                                                'exp': {'op':'-',
                                                        'g':{'var':'y'},
                                                        'd':{'var':'x'}}}}}}}

                                                
   
              
      
   
print('1',isexparith({'int': 4}))

print('2',isexparith({'op':'+','g':{'var':'x'},'d':{'int':4}}))

print('3',isprog(prog))

def evalarith(exp,env):
  if sorted(exp.keys()) == ['var']:
    return search(exp['var'],env)
  elif sorted(exp.keys()) == ['int']:
    return exp['int']
  elif sorted(exp.keys()) == ['d','g','op']:
    if exp['op'] == '+':
      return evalarith(exp['g'],env) + evalarith(exp['d'],env)
    elif exp['op'] == '-':
      return evalarith(exp['g'],env) - evalarith(exp['d'],env)
    elif exp['op'] == '*':
      return evalarith(exp['g'],env) * evalarith(exp['d'],env)
    else:
      raise Erreur_Evaluation

  
def evalbool(exp,env):
  if sorted(exp.keys()) == ['bool']:
    if exp['bool'] == 'true':
      return True
    else:
      return False
  elif sorted(exp.keys()) == ['comp','d','g']:
    if exp['comp'] == '=':
      return evalarith(exp['g'],env) == evalarith(exp['d'],env)
    else:
      return evalarith(exp['g'],env) <= evalarith(exp['d'],env)
  elif sorted(exp.keys()) == ['neg']:
    return not (evalbool(exp['neg'],env))
  elif sorted(exp.keys()) ==['arg1','arg2','opbin']:
    if exp['opbin'] == 'and':
      return evalbool(exp['arg1'],env) and evalbool(exp['arg2'],env)
    else:
      return evalbool(exp['arg1'],env) or evalbool(exp['arg2'],env)


    
def evalprog(exp,env):
  if sorted(exp.keys()) == ['skip']:
    return env
  elif sorted(exp.keys()) == ['exp','var']:
    print('var',env)
    return insert(evalarith(exp['exp'],env),exp['var'],env)
  elif sorted(exp.keys()) == ['c1','c2']:
    env = evalprog(exp['c1'],env)
    print('seq',env)
    return evalprog(exp['c2'],env)
  elif sorted(exp.keys()) == ['cond','else','then']:
    if evalbool(exp['cond'],env):
      return evalprog(exp['then'],env)
    else:
      return evalprog(exp['else'],env)
  elif sorted(exp.keys()) == ['cond','whiledo']:
    if evalbool(exp['cond'],env):
      env = evalprog(exp['whiledo'],env)
      return evalprog(exp,env)
    else :
      return env
    
                
  
