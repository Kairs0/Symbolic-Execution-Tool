from constraint import *
# ['(x4==1)', 'x2=0-x1', '(x1<=0)']
problem = Problem()
problem.addVariable('x1', range(-1, 1))
problem.addVariable('x2', range(-1, 1))
# problem.addVariable('x4', range(5))
# exec('problem.addConstraint(lambda x1, x2, x4: (x4 == 1))')
# exec('problem.addConstraint(lambda x1, x2, x4: x2 == x4)')
# exec('problem.addConstraint(lambda x1, x2, x4: x2 == 0-x1)')
exec('problem.addConstraint(lambda x1, x2: not (x1 == 0))')
print(problem.getSolutions())

