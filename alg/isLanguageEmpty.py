from grammar import Grammar
from mytoken import *
from mytoken import MyToken as Token

def makeGrammarWithCoolRules(Grammar: Grammar, coolN: set[Token]) -> Grammar:
    coolRules = dict()
    for nonterm in coolN:
        coolRules[nonterm] = set()
        for rule in Grammar.P[nonterm]:
            ruleSet = set(rule)
            ruleLen = len(ruleSet)
            # Пересечение терминалов грамматики и терминалов правила
            TIntersect = Grammar.T.intersection(ruleSet)
            lenTIntersect = len(TIntersect)
            # Пересечение полезных нетерминалов и нетерминалов правила
            NIntersect = coolN.intersection(ruleSet)
            lenNIntersect = len(NIntersect)

            if (lenTIntersect == ruleLen) or ((lenNIntersect + lenTIntersect) == ruleLen):
                coolRules[nonterm].add(rule)
    return Grammar(set([i.symbol for i in coolN]), Grammar.getT(), coolRules, Grammar.S.symbol)

def isLanguageEmpty(Grammar: Grammar) -> tuple[bool, Grammar]:
    # Шаг 1
    N0 = set()
    N1 = set()
    while True:
        # Берём нетерминал, из которого можно что-то вывести по правилу
        for nonterm in Grammar.P:
            for rule in Grammar.P[nonterm]:
                ruleSet = set(rule)
                ruleLen = len(ruleSet)
                # Пересечение терминалов грамматики и терминалов правила
                TIntersect = Grammar.T.intersection(ruleSet)
                lenTIntersect = len(TIntersect)
                # Пересечение полезных нетерминалов и нетерминалов правила
                NIntersect = N0.intersection(ruleSet)
                lenNIntersect = len(NIntersect)

                if (lenTIntersect == ruleLen) or ((lenNIntersect + lenTIntersect) == ruleLen):
                    # Шаг 2: если из нетерминала nonterm выводится чистая строка терминалов,
                    N1.add(nonterm)
                    # Либо строка терминалов и полезных нетерминалов, то добавляем текущий нетерминал в список полезных нетерминалов
                    break
        # Шаг 3
        if N0 == N1:
            break
        else:
            N0 = N1.copy()
    # Шаг 4
    if Grammar.S in N1:
        return False, makeGrammarWithCoolRules(Grammar, N1)
    else:
        return True, Grammar
