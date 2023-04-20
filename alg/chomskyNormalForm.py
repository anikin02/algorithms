from grammar import Grammar as Grammar
from mytoken import *
from mytoken import MyToken as Token

def termToNonTerm(term: Token) -> Token:
    return Token(TOKEN_NONTERM, term.symbol + "`")

def processRule(nonterm: Token, rule: tuple) -> dict[Token, tuple]:
    result = dict()
    if len(rule) > 2:
        left = rule[0]
        right = rule[1:]
        rightSymbol = Token(TOKEN_NONTERM, "".join([i.symbol for i in right]))
        res = processRule(rightSymbol, right)
        if left.isTerm():
            newLeft = termToNonTerm(left)
            result[newLeft] = (left,)
            left = newLeft
        result[nonterm] = (left, rightSymbol)
        result.update(res)
    else:
        lt = rule[0].isTerm()
        rt = rule[1].isTerm()
        left = rule[0]
        right = rule[1]

        if lt:
            newLeft = termToNonTerm(left)
            result[newLeft] = (left,)
            left = newLeft
        if rt:
            newRight = termToNonTerm(right)
            result[newRight] = (right,)
            right = newRight
        result[nonterm] = (left, right)
    
    return result
        

def chomskyNormalForm(grammar: Grammar) -> Grammar:
    # Словарь с подходящими правилами
    newRules = dict()
    # Словарь с неподходящими правилами
    rulesToProcess = dict()
    newNonTerms = grammar.N.copy()

    # Заполнение словарей
    for nonterm in grammar.P:
        newRules[nonterm] = set()
        badRules = set()
        for rule in grammar.P[nonterm]:
            rulelen = len(rule)
            if rulelen == 2 and rule[0].isNonTerm() and rule[1].isNonTerm():
                newRules[nonterm].add(rule)
            elif rulelen == 1 and rule[0].isTerm():
                newRules[nonterm].add(rule)
            else:
                badRules.add(rule)
        if len(badRules) > 0:
            rulesToProcess[nonterm] = badRules.copy()
    
    for nonterm in rulesToProcess:
        for rule in rulesToProcess[nonterm]:
            processed = processRule(nonterm, rule)
            keys = processed.keys()
            newNonTerms.update(keys)
            for key in keys:
                if key not in newRules:
                    newRules[key] = set()
                newRules[key].add(processed[key])

    return Grammar(set([i.symbol for i in newNonTerms]), grammar.getT() , newRules, grammar.getS())