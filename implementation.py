"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
import itertools
import re
import helpers

def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:
    result = set()
    count = constraint_pattern.count("{}")
    combinations = itertools.product(nonterminals,repeat=count)
    for group in combinations:
        result.add(constraint_pattern.format(*group))
    return result

def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:
    result = set()
    subtrees_dict = {}
    non_terminals = re.findall(r"(<[^>]+>)", abstract_constraint)
    for symbol in nts_to_subtrees:
        subtrees_dict[symbol] = []
        for _,subtrees in nts_to_subtrees[symbol]:
            for child_name,_ in subtrees:
                subtrees_dict[symbol].append(child_name)
    input_lists = []
    for symbol in non_terminals:
        abstract_constraint = abstract_constraint.replace(symbol,"{}")
        input_lists.append(subtrees_dict[symbol])
    combinations = itertools.product(*input_lists,repeat=len(input_lists))
    for group in combinations:
        result.add(abstract_constraint.format(*group))
    return result

def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:
    pass

def check(abstract_constraints: set[str], derivation_tree) -> bool:
    pass

def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:
    pass