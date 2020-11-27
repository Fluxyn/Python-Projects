import re
from tabulate import tabulate
from more_itertools import collapse

def lex(code, tokendict):
    '''Lex raw sorce code into tokens.'''
    tmp = []
    for t in tokendict.values():
        if isinstance(t, list):
            tmp.append(f'\{t[0]}.*?\{t[1]}')
    splitcode = re.split(fr"(\d+|\w*|{'|'.join(tmp)}|'.*?'|)", (code + '\n'))
    tmplist = []
    for token in splitcode:
        new_token = token.replace(' ', '')
        tmplist.append(new_token)
    splitcode = [str for str in tmplist if str]
    tokens = []
    for t in splitcode:
        for s in tokendict:
            if isinstance(tokendict[s], str):
                if t in tokendict[s]:
                    tokens.append(s)
                    break
            elif isinstance(tokendict[s], list) and len(tokendict[s]) == 2:
                if t.startswith(tokendict[s][0]) == True and t.endswith(tokendict[s][1]) == True:  
                    tokens.append(s)
                    break
            else:
                try:
                    if tokendict[s] == type(eval(t)):
                        tokens.append(s)
                        break
                except:
                    if tokendict[s] == type(t):
                        tokens.append(s)
                        break
    splitcode.append('')
    tokens.append('EOF')
    res = splitcode, tokens
    return res

def parse(lexedcode, exprdict, funcdict, tokendict):
    '''Parse lexed code and tokens into an ast.'''
    ast = {}
    for a in range(len(lexedcode[0])):
        for i in range(len(lexedcode[1])-2):
            for s in exprdict:
                    tmp = (' + " " + '.join([f'lexedcode[1][{r+i}]' for r in range(len(s.split()))]))
                    if eval(tmp) == s:
                        tmp = {}
                        for t in s.split():
                            pattern = lexedcode[0][[r+i for r in range(len(s.split()))][0]:[r+i for r in range(len(s.split()))][-1]+1]
                            if s.split().count(t) > 1:
                                tmp[t] = ([pattern[i] for i in [i for i, x in enumerate(s.split()) if x == t]])
                            else:
                                tmp[t] = pattern[s.split().index(t)]
                        patterntmp = exprdict[s]
                        for t in set(s.split()):
                            if isinstance(tmp[t], list):
                                for n in range(s.split().count(t)):
                                    patterntmp = patterntmp.replace(t, f"{{tmp['*'][{n}]}}", 1)
                            else:
                                patterntmp = patterntmp.replace(t, f"{{tmp['{t}']}}")
                            patterntmp = patterntmp.replace('*', t)
                        ast[(eval(f'f"{patterntmp}"'))] = 'expr'
            for s in funcdict:
                    tmp = (' + " " + '.join([f'lexedcode[1][{r+i}]' for r in range(len(s.split()))]))
                    if eval(tmp) == s:
                        tmp = {}
                        for t in s.split():
                            pattern = lexedcode[0][[r+i for r in range(len(s.split()))][0]:[r+i for r in range(len(s.split()))][-1]+1]
                            if t == s.split()[1]:
                                if isinstance(eval(pattern[s.split().index(t)]), str):
                                    tmp[t] = tokendict['STRING'][0] + eval(pattern[s.split().index(t)]) + tokendict['STRING'][1]
                                else:
                                    tmp[t] = eval(pattern[s.split().index(t)])
                            elif s.split().count(t) > 1:
                                tmp[t] = ([pattern[i] for i in [i for i, x in enumerate(s.split()) if x == t]])
                            else:
                                tmp[t] = pattern[s.split().index(t)]
                        patterntmp = funcdict[s]
                        for t in set(s.split()):
                            if isinstance(tmp[t], list):
                                for n in range(s.split().count(t)):
                                    patterntmp = patterntmp.replace(t, f"{{tmp['*'][{n}]}}", 1)
                            else:
                                patterntmp = patterntmp.replace(t, f"{{tmp['{t}']}}")
                            patterntmp = patterntmp.replace('*', t)
                        ast[(eval(f'f"{patterntmp}"'))] = 'func'
        return ast

def generate(ast, tokens, funcpatternlist):
    '''Generate simple, python-like bytecode from an ast.'''
    bytecodelist = [
    'BINARY_ADD',
    'BINARY_SUB',
    'BINARY_MUL',
    'BINARY_DIV',
    'LOAD_CONST',
    'LOAD_GLOBAL',
    'PRINT_ITEM'
    ]
    funcpatterns = {
    'BINARY_ADD': '''[['LOAD_CONST', pattern[1]], ['LOAD_CONST', pattern[2]], ['BINARY_ADD']]''',
    'BINARY_SUB': '''[['LOAD_CONST', pattern[1]], ['LOAD_CONST', pattern[2]], ['BINARY_SUB']]''',
    'BINARY_MUL': '''[['LOAD_CONST', pattern[1]], ['LOAD_CONST', pattern[2]], ['BINARY_MUL']]''',
    'BINARY_DIV': '''[['LOAD_CONST', pattern[1]], ['LOAD_CONST', pattern[2]], ['BINARY_DIV']]''',
    }
    bytecode = []
    consts = []
    for func in ast:
        pattern = func.replace(',', '').split()
        pattern = str(pattern).replace('(', '')
        pattern = pattern.replace(')', '')
        pattern = pattern.replace('', '')
        pattern = eval(pattern)
        if pattern[0] in list(tokens.values()):
            bytecode.extend(eval(funcbytecode[list(tokens.keys())[list(tokens.values()).index(pattern[0])]]))
        else:
            bytecode.extend(eval(funcpatterns[pattern[0]]))
    print(tabulate(bytecode, tablefmt='plain'))
    return list(collapse(bytecode))

def interpret(bytecode):
    '''Interpret and execute bytecode.'''
    bytecodeparameters = {
    'BINARY_ADD': 0,
    'BINARY_SUB': 0,
    'BINARY_MUL': 0,
    'BINARY_DIV': 0,
    'LOAD_CONST': 1,
    'LOAD_GLOBAL': 1,
    'PRINT_ITEM': 0
    }
    for c in bytecode:
        if c in bytecodeparameters.keys():
            print(bytecode[bytecode.index(c):(bytecodeparameters[c]+1)+bytecode.index(c)])
        
          

code = '''print(1+2)'''

tokens = {
    'STRING': ['"', '"'],
    'PAREN': ['(', ')'],
    'COMMENT': ['#', '\n'],
    'PLUS' : '+',
    'SUBTRACT' : '-',
    'MULTIPLY' : '*',
    'DIVIDE' : '/',
    'EOL': '\n',
    'NUM': int,
    'NAME': str,
    'PRINT': 'print'
}

exprdict = {
    'NUM PLUS NUM': 'BINARY_ADD (NUM), (NUM)',
    'NUM SUBTRACT NUM': 'BINARY_SUB (NUM), (NUM)',
    'NUM MULTIPLY NUM': 'BINARY_MUL (NUM), (NUM)',
    'NUM DIVIDE NUM': 'BINARY_DIV (NUM), (NUM)',
}

funcdict = {
    'PRINT PAREN': 'PRINT (PAREN)',
}

funcbytecode = {
    'PRINT': '''[['LOAD_CONST', pattern[1]], ['PRINT_ITEM']]''',
}

print(interpret(generate(parse(lex(code, tokens), exprdict, funcdict, tokens), tokens, funcbytecode)))

