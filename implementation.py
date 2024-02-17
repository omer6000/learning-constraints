"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
import itertools
import helpers
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer
# import re

def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:
    result = set()
    count = constraint_pattern.count("{}")
    combinations = itertools.product(nonterminals,repeat=count)
    for group in combinations:
        result.add(constraint_pattern.format(*group))
    return result

def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:
    # result = set()
    # subtrees_dict = {}
    # non_terminals = re.findall(r"(<[^>]+>)", abstract_constraint)
    # for symbol in nts_to_subtrees:
    #     subtrees_dict[symbol] = []
    #     for _,subtrees in nts_to_subtrees[symbol]:
    #         for child_name,_ in subtrees:
    #             subtrees_dict[symbol].append(child_name)
    # input_lists = []
    # for symbol in non_terminals:
    #     abstract_constraint = abstract_constraint.replace(symbol,"{}")
    #     input_lists.append(subtrees_dict[symbol])
    # combinations = itertools.product(*input_lists,repeat=len(input_lists))
    # for group in combinations:
    #     result.add(abstract_constraint.format(*group))
    # return result

    non_terminals = []
    for non_terminal in nts_to_subtrees:
        if abstract_constraint.find(non_terminal) != -1:
            non_terminals.append(non_terminal)
    n = len(non_terminals)
    result = set()
    if n == 2:
        for st1 in nts_to_subtrees[non_terminals[0]]:
            for st2 in nts_to_subtrees[non_terminals[1]]:
                result.add(abstract_constraint.replace(non_terminals[0],helpers.tree_to_string(st1)).replace(non_terminals[1],helpers.tree_to_string(st2)))
        return result
    elif n == 1:
        for subtree in nts_to_subtrees[non_terminals[0]]:
            result.add(abstract_constraint.replace(non_terminals[0],helpers.tree_to_string(subtree)))
        return result
    else:
        return result

def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:
    non_terminals = {}
    for tree in derivation_trees:
        non_terms = helpers.get_all_subtrees(tree).keys()
        for non_term in non_terms:
            if non_term in non_terminals:
                non_terminals[non_term] += 1
            else:
                non_terminals[non_term] = 1
    total_trees = len(derivation_trees)
    valid_non_terminals = []
    for non_term in non_terminals:
        if non_terminals[non_term] == total_trees:
            valid_non_terminals.append(non_term)
    instantiate_cons = set()
    for constraint_prn in constraint_patterns:
        instantiate_cons = instantiate_cons.union(instantiate_with_nonterminals(constraint_prn,valid_non_terminals))
    
    valid_cons = set()
    for init_constraint in instantiate_cons:
        valid = True
        for tree in derivation_trees:
            if check({init_constraint},tree) == False:
                valid = False
                break
        if valid:
            valid_cons.add(init_constraint)
    return valid_cons

def check(abstract_constraints: set[str], derivation_tree) -> bool:
    subtrees = helpers.get_all_subtrees(derivation_tree)
    for c in abstract_constraints:
        instantiate_w_subtrees = instantiate_with_subtrees(c,subtrees)
        check = False
        for i_constraint in instantiate_w_subtrees:
            try:
                if eval(i_constraint):
                    check = True
                    break
            except:
                pass
        if check == False:
            return False
    return True

def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:
    p = EarleyParser(grammar)
    fuzzer = EvenFasterGrammarFuzzer(grammar)
    notValid = True
    while notValid:
        input = fuzzer.fuzz()
        derivation_tree = next(p.parse(input))
        if check(abstract_constraints,derivation_tree) == produce_valid_sample:
            notValid = False
    return input