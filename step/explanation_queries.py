#!/usr/bin/env python

"""
compile the prime implicants of an SDD/BDD
"""

from collections import defaultdict
import sdd
from sdd import models

########################################
# PRIME IMPLICANTS
########################################
def _primes_one_given_term(alpha,variables,inst,cache,cache_dummy,pmgr,mgr):
    if len(variables) == 0:
        if sdd.sdd_node_is_true(alpha): return sdd.sdd_manager_true(pmgr)
        if sdd.sdd_node_is_false(alpha): return sdd.sdd_manager_false(pmgr)
    #add cases for true/false

    key = (len(variables),sdd.sdd_id(alpha))
    if key in cache:
        return cache[key]


    var,remaining = variables[0],variables[1:]
    val, remaining_val = inst[0],inst[1:]
    beta2 = sdd.sdd_forall(var,alpha,mgr)

    gamma2 = _primes_one_given_term(beta2,remaining,remaining_val,cache,cache_dummy,pmgr,mgr)
    gamma9 = gamma2
    pvar = 3*(var-1)+1
    kappa2 = sdd.sdd_manager_literal(-pvar,pmgr)
    gamma2 = sdd.sdd_conjoin(gamma2,kappa2,pmgr)

    if val == 0:
        beta0 = sdd.sdd_condition(-var,alpha,mgr)
        gamma0 = _primes_one_given_term(beta0,remaining,remaining_val,cache,cache_dummy,pmgr,mgr)
        gamma0 = sdd.sdd_conjoin(gamma0,sdd.sdd_negate(gamma9,pmgr),pmgr)
        kappa0 = sdd.sdd_conjoin(sdd.sdd_manager_literal(-(pvar+1),pmgr),
                                 sdd.sdd_manager_literal( (pvar+2),pmgr),pmgr)
        kappa0 = sdd.sdd_conjoin(kappa0,sdd.sdd_manager_literal(pvar,pmgr),pmgr)
        gamma0 = sdd.sdd_conjoin(gamma0,kappa0,pmgr)
        #gamma0 = sdd.sdd_conjoin(gamma0,sdd.sdd_negate(gamma9,pmgr),pmgr)

    if val == 1:
        beta1 = sdd.sdd_condition(var,alpha,mgr)
        gamma1 = _primes_one_given_term(beta1,remaining,remaining_val,cache,cache_dummy,pmgr,mgr)
        gamma1 = sdd.sdd_conjoin(gamma1,sdd.sdd_negate(gamma9,pmgr),pmgr)
        kappa1 = sdd.sdd_conjoin(sdd.sdd_manager_literal( (pvar+1),pmgr),
                                 sdd.sdd_manager_literal(-(pvar+2),pmgr),pmgr)
        kappa1 = sdd.sdd_conjoin(kappa1,sdd.sdd_manager_literal(pvar,pmgr),pmgr)
        gamma1 = sdd.sdd_conjoin(gamma1,kappa1,pmgr)
        #gamma1 = sdd.sdd_conjoin(gamma1,sdd.sdd_negate(gamma9,pmgr),pmgr)

    if val == 0:
        gamma = sdd.sdd_disjoin(gamma0,gamma2,pmgr)
    if val == 1:
        gamma = sdd.sdd_disjoin(gamma1,gamma2,pmgr)
    #gamma = sdd.sdd_disjoin(sdd.sdd_disjoin(gamma0, gamma1, pmgr), gamma2, pmgr)

    #if len(variables) > 60:
    #  print len(variables), sdd.sdd_manager_count(mgr)
    cache[key] = gamma
    return gamma

def _remove_dummies(alpha,var_count,pmgr):
    for var in xrange(1,var_count+1):
        var = 3*(var-1)+1
        beta = sdd.sdd_manager_literal(-var,pmgr)
        gamma = sdd.sdd_disjoin(sdd.sdd_manager_literal(var+1,pmgr),
                                sdd.sdd_manager_literal(var+2,pmgr),pmgr)
        beta = sdd.sdd_conjoin(beta,gamma,pmgr)
        alpha = sdd.sdd_conjoin(alpha,sdd.sdd_negate(beta,pmgr),pmgr)
    return alpha

def prime_to_term(prime,mgr):
    """converts a prime from the IP-SDD to a term in the original manager
    
    assumes prime is an IP-model (dict from var to value)"""
    var_count = sdd.sdd_manager_var_count(mgr)
    term = sdd.sdd_manager_true(mgr)
    for var in xrange(1,var_count+1):
        pvar = 3*(var-1)+1
        if prime[pvar] == 0: continue
        val = prime[pvar+1]
        lit = var if val == 1 else -var
        lit = sdd.sdd_manager_literal(lit,mgr)
        term = sdd.sdd_conjoin(term,lit,mgr)
    return term

def prime_to_dict(prime,var_count):
    """converts a prime from the IP-SDD to a term in the original manager
    
    assumes prime is an IP-model (dict from var to value)"""
    term = {}
    for var in xrange(1,var_count+1):
        pvar = 3*(var-1)+1
        if prime[pvar] == 0: continue
        val = prime[pvar+1]
        term[var] = val
    return term

# CHANGE DEFAULT PRIMES IMPLEMENTATION HERE:
def primes_given_term(alpha,inst,mgr,primes_f):
    var_count = sdd.sdd_manager_var_count(mgr)
    primes_var_count = 3*var_count
    primes_vtree = sdd.sdd_vtree_new(primes_var_count,"right")
    primes_mgr = sdd.sdd_manager_new(primes_vtree)
    variables = range(1,var_count+1)
    cache1,cache2 = {},{}
    kappa = primes_f(alpha,variables,inst,cache1,cache2,primes_mgr,mgr)
    kappa = _remove_dummies(kappa,var_count,primes_mgr)
    return kappa,primes_mgr,primes_vtree

# ENUMERATION BY SIZE
def enumerate_primes(primes,pmgr,var_count):
    pvtree = sdd.sdd_manager_vtree(pmgr)
    while not sdd.sdd_node_is_false(primes):
        mincard = sdd.sdd_global_minimize_cardinality(primes,pmgr)
        for model in models.models(mincard,pvtree):
            term = prime_to_dict(model,var_count)
            yield term
        primes = sdd.sdd_conjoin(primes,sdd.sdd_negate(mincard,pmgr),pmgr)

def primes_by_length(primes,pmgr,var_count):
    by_length = defaultdict(list)
    pvtree = sdd.sdd_manager_vtree(pmgr)
    for model in models.models(primes,pvtree):
        term = prime_to_dict(model,var_count)
        by_length[len(term)].append(term)
    return by_length

def run_prime_implicant_query(alpha, mgr, num_features, models_list):
    print num_features, models_list
    for model_list in models_list:
        gamma,pmgr,pvtree2 = primes_given_term(alpha,model_list,mgr,_primes_one_given_term)
        pvtree = sdd.sdd_manager_vtree(pmgr)
        pi_str = []

        gamma = sdd.sdd_global_minimize_cardinality(gamma, pmgr) 
        for prime_model in models.models(gamma,pvtree):
            try:
                term = prime_to_dict(prime_model,num_features)
                term_str = " ".join([ ("*" if var not in term else "1" if term[var] == 1 else "0") for var in xrange(1,num_features+1) ])
                pi_str.append(term_str)
            except:
                pi_str = ["Key error. Make sure instance is is a model of the SDD."]
        pi_str.sort(key=lambda x: x.count('*'), reverse=True)
        
        print "Model: " + str(model_list) + ""
        print "PI explanations:"
        for pi in pi_str:
          print str(pi)

        sdd.sdd_vtree_free(pvtree2)
        sdd.sdd_manager_free(pmgr)

########################################
# ROBUSTNESS
########################################
def run_robustness_query(alpha, mgr, num_features, models_list):
  max_robustness = 0

  for model in models_list:
    flips, counterexample = least_flips(alpha,mgr,model)
    print "Model: \t\t\t", model
    print "Counterexample: \t", counterexample, "Flips: " + str(flips)

# assumes right linear vtree (OBDD)
my_inf = 1000000000
def least_flips_helper(is_model,inst,alpha,mgr, leastFlipsDict):
  sid = sdd.sdd_id(alpha)
  
  if sid in leastFlipsDict.keys():
    return leastFlipsDict[sid]

  flip_inst = inst[:]

  if sdd.sdd_node_is_true(alpha):
    return (my_inf, flip_inst) if is_model else (0, flip_inst)
  elif sdd.sdd_node_is_false(alpha):
    return (0, flip_inst) if is_model else (my_inf, flip_inst)

  if sdd.sdd_node_is_literal(alpha):
    level = abs(sdd.sdd_node_literal(alpha))-1
    if (inst[level] == 1) == (sdd.sdd_node_literal(alpha) > 0):
      if is_model:
        flip_inst[level] = 1-inst[level]
        return (1, flip_inst)
      else:
        return (0, flip_inst)
    else:
      if is_model:
        return (0, flip_inst)
      else:
        flip_inst[level] = 1-inst[level]
        return (1, flip_inst)
 
  node_elements = sdd.sdd_node_elements(alpha)
  m = sdd.sdd_node_size(alpha)
  assert m == 2

  prime1 = sdd.sddNodeArray_getitem(node_elements,0)
  sub1 = sdd.sddNodeArray_getitem(node_elements,1)
  prime0 = sdd.sddNodeArray_getitem(node_elements,2)
  sub0 = sdd.sddNodeArray_getitem(node_elements,3)

  if sdd.sdd_node_literal(prime1) < 0:
    prime1, prime0 = prime0, prime1
    sub1, sub0 = sub0, sub1

  level = abs(sdd.sdd_node_literal(prime1)) - 1

  result1, flip_inst1 = least_flips_helper(is_model, inst, sub1, mgr, leastFlipsDict)
  result0, flip_inst0 = least_flips_helper(is_model, inst, sub0, mgr, leastFlipsDict)

  if (result1 + (int)(inst[level] != 1)) < (result0 + (int)(inst[level] != 0)):
    result, flip_inst = result1 + (int)(inst[level] != 1), flip_inst1[:]
    if inst[level] == 0:
      flip_inst[level] = 1
  else:
    result, flip_inst = result0 + (int)(inst[level] != 0), flip_inst0[:]
    if inst[level] == 1:
      flip_inst[level] = 0

  leastFlipsDict[sid] = (result, flip_inst)
  return (result, flip_inst)

def least_flips(alpha,mgr,inst):
  beta = alpha
  for (i, element) in enumerate(inst):
    literal = i+1
    if element == 0:
      literal *= -1
    beta = sdd.sdd_condition(literal,beta,mgr);
  is_model = sdd.sdd_node_is_true(beta)
  leastFlipsDict = {}
  return least_flips_helper(is_model, inst, alpha, mgr, leastFlipsDict)


########################################
# MONOTONICITY
########################################


def run_monotonic_query(alpha,mgr,num_features,constraint_sdd=None):
  if not constraint_sdd:
    constraint_sdd = sdd.sdd_manager_true(mgr)

  monotonicity, counterexample = is_monotonic(alpha, mgr, num_features,constraint_sdd)
  print "Is sdd monotonic?: " + str(monotonicity)

  print "Output counterexamples for monotonicity for each variable, if any."
  for (i,c) in enumerate(counterexample):
    print "Counterexample for var " + str(i) + ", with positive as 0: " + str(c[0])
    print "Counterexample for var " + str(i) + ", with positive as 1: " + str(c[1])

# assumes right linear vtree (OBDD)
def is_monotonic(alpha,mgr,num_features,constraint_sdd):

  counterexample = [[None, None] for _ in xrange(num_features)]
  for i in xrange(num_features):
    beta1 = sdd.sdd_condition(i+1, alpha, mgr)
    beta2 = sdd.sdd_condition(-(i+1), alpha, mgr)
    beta3 = sdd.sdd_conjoin(beta1, beta2, mgr)

    # check if f|x does not entail f|!x
    gamma = sdd.sdd_conjoin(sdd.sdd_conjoin( sdd.sdd_negate(beta2, mgr), beta1, mgr), constraint_sdd, mgr)
    model = next(models.models( gamma, sdd.sdd_manager_vtree(mgr)))
    counterexample[i][0] = [v for _,v in model.items()]
    if counterexample[i][0]:
      counterexample[i][0][i] = 1

    # check if f|!x does not entail f|x
    gamma = sdd.sdd_conjoin(sdd.sdd_conjoin( sdd.sdd_negate(beta1, mgr), beta2, mgr), constraint_sdd, mgr)
    model = next(models.models( gamma, sdd.sdd_manager_vtree(mgr)))
    counterexample[i][1] = [v for _,v in model.items()]
    if counterexample[i][1]:
      counterexample[i][1][i] = 0

  for c in counterexample:
    if c[0] and c[1]:
      return False, counterexample
  return True, counterexample

########################################
# UNUSED_VARS
########################################

def run_unused_vars_query(alpha,mgr,num_features):
  unused_vars = []
  for i in xrange(num_features):
    if alpha == sdd.sdd_forall((i+1), alpha, mgr):
      unused_vars.append(i)
  if not unused_vars:
    print "No unused variables."
  else:
    print "Unused variables: " + str(unused_vars)

########################################
# MIN_CARD
########################################
def condition_and_minimize(alpha,mgr,num_features,inst):
  for i in xrange(num_features):
    if not inst[i]:
      alpha = sdd.sdd_condition(-1*(i+1),alpha,mgr)
  # After conditioning, the literals can be T or F.
  # After we do global_minimize_cardinality that forces the conditioned
  # literals to be F.
  return sdd.sdd_global_minimize_cardinality(alpha,mgr)

def run_mincard_query(alpha,mgr,num_features,models_list):
  for model in models_list:
    beta = condition_and_minimize(alpha, mgr, num_features, model)
    vtree = sdd.sdd_manager_vtree(mgr)
    print "Model: ", model
    print "MC Explanations: "
    for model in sdd.models.models(beta,vtree):
      print sdd.models.str_model(model)
