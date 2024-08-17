#!/bin/env python3
from lark import Lark, Token, Transformer, Discard, Visitor
import argparse

# Define the grammar
grammar = r"""
    start: (SPACES? (rule_statement | set_definition | comment)? WHITESPACES?)*

    comment: /#.*/

    rule_statement: NAME "->" rule ("|" rule)*
    rule: (NAME ":")* rule_content
    rule_content: rule_atom ("," rule_atom)* ","?
    rule_atom: ATOM | terminal | string | non_terminal | semantic_action

    terminal: NAME | "*" NAME | NAME EPSILON ATOM
    string: "\"" TEXT "\""
    TEXT: /((\\.)|[^"])+/
    non_terminal: "<" NAME ">"
    semantic_action: "[" NAME "]"

    set_definition: NAME "=" minus_sigma? "{" set_contents "}"
    minus_sigma: "sigma" "-"
    set_contents: ATOM ("," ATOM)* ","?
    
    NAME: /[a-zA-Z_0-9]+/
    EPSILON: "@"
    ATOM: /\\?[^\s]/
    SPACES: /[ \t\f]+/
    WHITESPACES: /\s+/ 
    %ignore WHITESPACES
"""

class SpaceTransformer(Transformer):
    def WHITESPACES(self, tok: Token):
        return Discard
    def SPACES(self, tok: Token):
        return Discard

class ItemTransformer(Transformer):
    def rule_atom(self, children):
        return children[0]

def parse_args():
    parser = argparse.ArgumentParser(description="Desatomat is a parser compiler which outputs C++")

    # Add flags with True as default, and allow setting them to False
    parser.add_argument('--ll', action='store_false', default=True, help='Enable or disable ll flag')
    parser.add_argument('--q', action='store_false', default=True, help='Enable or disable q flag')

     # Add standard arguments with defaults
    parser.add_argument('--input', type=argparse.FileType('r'), required=True, help='Input file path or "-" for stdin')
    parser.add_argument('--output', type=str, default='.', help='Output directory')
    parser.add_argument('--generator', type=str, default='cpp_ctll_v2', help='Generator to use')
    
    # Add configuration arguments
    parser.add_argument('--cfg:fname', type=str, default="grammer.hpp", help='Output filename')
    parser.add_argument('--cfg:namespace', type=str, default="Grammer", help='C++ namespace to put the grammer in')
    parser.add_argument('--cfg:guard', type=str, help='C++ header guard name')
    parser.add_argument('--cfg:grammar_name', type=str, default="Grammer", help='C++ grammar struct name')

    # Parse arguments
    args = parser.parse_args()
    return args

identifier_table={
    "nonterminal":{},
    "terminal":{
        'epsilon':'',
        'other':''
    }
}

class add_identifers(Visitor):
    def set_definition(self, tree):
        # set_definition.children     -> NAME, minus_sigma, set_contents
        # set_definition.children[-1] -> set_contents
        # set_definition.set_contents.children -> ATOM, ATOM, ATOM, ...
        #   minus_sigma not guaranteed to be in set_definition's children.
        #   Anyway, CTRE does not use minus_sigma so we are ignoring it
        NAME = tree.children[0]
        ATOMS = tree.children[-1].children

        # Turn Token('ATOM', CHAR) into a list of CHAR-s
        res = [token.value for token in ATOMS]

        # Ignore the '\' at the beginning of the string
        res = [token if token[0] != '\\' else token[-1] for token in res]

        # Convert list to string (easier to read for debugging)
        res = "".join(res)

        identifier_table["terminal"][NAME.value] = res

    def rule_statement(self, tree):
        # rule_statement.children        -> NAME, rule, rule, rule ... 
        # rule_statement.children[0]     -> NAME
        # rule_statement.children[1:]    -> rule, rule, rule, ...
        # rule_statement.children[1:][X].children -> NAME, rule_content
        #rules = tree.children[1:]
        #res = []
        #identifier_table[tree.children[0].value] = tree.children[1:]
        pass

class verify_identifiers(Visitor):
    def terminal(self, tree):
        # Terminal value
        tok = tree.children[0].value
        # For some reason ATOMS are being translated as terminals
        # Hack: Skip over single character ATOMS
        if len(tok) != 1:
            if not tok in identifier_table["terminal"]:
                raise Exception(f"Unknown identifier {tok}")
            
    def non_terminal(self, tree):
        pass

if __name__ == "__main__":
    args = parse_args()

    with args.input as input_file:
        input_data = input_file.read() 
    
    parser = Lark(grammar, start='start')
    tree = parser.parse(input_data)
    tree = (SpaceTransformer()*ItemTransformer()).transform(tree)
    (add_identifers()).visit(tree)
    # Convert terminal character list into strings
    (verify_identifiers()).visit(tree)
    #print(tree)
    #print(tree.pretty())
    #import pprint
    #pprint.pp(identifier_table)
