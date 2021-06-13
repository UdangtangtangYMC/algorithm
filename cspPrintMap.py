from copy import deepcopy
from itertools import product
from simpleai.search.utils import argmin
from simpleai.search import CspProblem, \
        min_conflicts, MOST_CONSTRAINED_VARIABLE, \
        HIGHEST_DEGREE_VARIABLE, LEAST_CONSTRAINING_VALUE

from simpleai.search import csp

class Log:
  def __init__(self):
    self.log_list = []

  def delete(self):
    self.log_list = []

  def update(self, assignment):
    self.log_list.append(assignment)

  def print_log(self):
    print('print all step')

    for i, log in enumerate(self.log_list):
      print('{} step : '.format(i), end='')
      print(log)

  def print_cnt(self):
    print('total step : {}'.format(len(self.log_list)))

  def print(self):
    self.print_log()
    self.print_cnt()


def backtrack(problem, variable_heuristic='', value_heuristic='', inference=True, log=None):
    '''
    Backtracking search.
    variable_heuristic is the heuristic for variable choosing, can be
    MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE, or blank for simple
    ordered choosing.
    value_heuristic is the heuristic for value choosing, can be
    LEAST_CONSTRAINING_VALUE or blank for simple ordered choosing.
    '''
    assignment = {}
    domains = deepcopy(problem.domains)

    if variable_heuristic == csp.MOST_CONSTRAINED_VARIABLE:
        variable_chooser = csp._most_constrained_variable_chooser
    elif variable_heuristic == csp.HIGHEST_DEGREE_VARIABLE:
        variable_chooser = csp._highest_degree_variable_chooser
    else:
        variable_chooser = csp._basic_variable_chooser

    if value_heuristic == csp.LEAST_CONSTRAINING_VALUE:
        values_sorter = csp._least_constraining_values_sorter
    else:
        values_sorter = csp._basic_values_sorter
    return _backtracking(problem,
                         assignment,
                         domains,
                         variable_chooser,
                         values_sorter,
                         inference=inference,
                         log=log)
    
def _backtracking(problem, assignment, domains, variable_chooser, values_sorter, inference=True, log=None):
    '''
    Internal recursive backtracking algorithm.
    '''
    from simpleai.search.arc import arc_consistency_3

    if log is not None:
          log.update(assignment)
    
    if len(assignment) == len(problem.variables):
        return assignment

    pending = [v for v in problem.variables
               if v not in assignment]
    variable = variable_chooser(problem, pending, domains)

    values = values_sorter(problem, assignment, variable, domains)

    for value in values:
        new_assignment = deepcopy(assignment)
        new_assignment[variable] = value

        if not csp._count_conflicts(problem, new_assignment):  # TODO on aima also checks if using fc
            new_domains = deepcopy(domains)
            new_domains[variable] = [value]

            if not inference or arc_consistency_3(new_domains, problem.constraints):
                result = _backtracking(problem,
                                       new_assignment,
                                       new_domains,
                                       variable_chooser,
                                       values_sorter,
                                       inference=inference,
                                       log=log)
                if result:
                    return result

    return None

def constraint_not_same(variables, values):
    return values[0] != values[1]


if __name__=='__main__':
    variables = ('WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T')

    domains = {
      'WA' : ['Red','Blue','Green'],
      'NT' : ['Red','Blue','Green'],
      'SA' : ['Red','Blue','Green'],
      'Q' : ['Red','Blue','Green'],
      'NSW' : ['Red','Blue','Green'],
      'V' : ['Red','Blue','Green'],
      'T' : ['Red','Blue','Green']
    }

    constraints = [
     (('WA','NT'),constraint_not_same),
     (('WA','SA'),constraint_not_same),
     (('NT','SA'),constraint_not_same),
     (('NT','Q'),constraint_not_same),
     (('SA','Q'),constraint_not_same),
     (('SA','NSW'),constraint_not_same),
     (('SA','V'),constraint_not_same),
     (('Q','NSW'),constraint_not_same),
     (('NSW','V'),constraint_not_same)
    ]

    log = Log()
    problem = CspProblem(variables, domains, constraints)
    
    print('\nMost constrained variable and least constraining value:\n', 
          backtrack(problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, 
          value_heuristic=LEAST_CONSTRAINING_VALUE, log=log))
    log.print()
    log.delete()