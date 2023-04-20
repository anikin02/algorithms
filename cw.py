# Решение для Esolang Interpreters #1 - Introduction to Esolangs and My First Interpreter (MiniStringFuck)
def my_first_interpreter(code):
    i = 0
    message = ''
    for n in code:
        if n in '+':
            i = (i + 1) % 256
        elif n in '.':
            message += chr(i)
    return message

# Решение для Esolang Interpreters #2 - Custom Smallfuck Interpreter
def interpreter(code, tape):
    bracketPos = {}
    stack = []
    for i, v in enumerate(code):
        if v in '[':
            stack.append(i)
        elif v in ']':
            if len(stack) != 0:
                previous = stack.pop()
                bracketPos[previous] = i
                bracketPos[i] = previous

    ptr = 0
    mem = list(map(int, tape))
    i = 0
    while 0 <= i < len(code):
        if ptr >= len(mem) or ptr < 0:
            break
        v = code[i]
        if v in '>':
            ptr += 1
        elif v in '<':
            ptr -= 1
        elif v in '*':
            mem[ptr] = 0 if mem[ptr] == 1 else 1
        elif v in '[':
            i = bracketPos[i] if mem[ptr] == 0 else i
        elif v in ']':
            i = bracketPos[i] if mem[ptr] != 0 else i
        i += 1
    return ''.join(map(str, mem))

# Решение для Esolang Interpreters #3 - Custom Paintfuck Interpreter
def interpreter(code, iterations, width, height):
    grid = [[0 for r in range(width)] for c in range(height)]
    t = iterations
    stack = []
    bracket_pos = {}
    for i, c in enumerate(code):
        if c == "[": 
            stack.append(i)
        elif c == "]": 
            bracket_pos[i] = stack[-1]
            bracket_pos[stack.pop()] = i

    a, b, p = 0, 0, 0    
    while t > 0 and p < len(code):
        if code[p] == "e": b += 1
        elif code[p] == "w": b -= 1
        elif code[p] == "s": a += 1
        elif code[p] == "n": a -= 1
        elif code[p] == "*": grid[a%height][b%width] ^= 1
        
        elif code[p] == "[":
            if grid[a%height][b%width] == 0:
                p = bracket_pos[p]
        elif code[p] == "]":
            if grid[a%height][b%width] == 1: 
                p = bracket_pos[p]
        else: t += 1
        t -= 1
        p += 1
    return "\r\n".join("".join(map(str, g)) for g in grid)

# Решение для Esolang Interpreters #4 - Boolfuck Interpreter
def boolfuck(code, input=""):
    myList = list(map(int, ''.join([bin(ord(i))[2:].rjust(8, '0')[::-1] for i in input])))
    var = {'mem': [0], 'ptr': 0, 'i': myList, 'iptr': 0, 'out': ''}
    new_code = []
    indent = 0
    for c in code:
        cur_indent = indent
        if c == '>': line = 'ptr += 1; ptr < len(mem) or mem.append(0)'
        elif c == '<': line = 'ptr -= 1; ptr >= 0 or mem.insert(0, 0)'
        elif c == '+': line = 'mem[ptr] = (mem[ptr] + 1) % 2'
        elif c == ';': line = 'out += str(mem[ptr])'
        elif c == ',': line = 'mem[ptr] = 0 if len(i) == 0 else i.pop(0)'
        elif c == '[': line = 'while mem[ptr]:'; indent += 1
        elif c == ']': line = ''; indent -= 1
        else: line = ''
        new_code.append('\t' * cur_indent + line)
    exec('\n'.join(new_code), var)

    out = var["out"]
    result = ""
    while out:
        result += chr(int(out[:8].ljust(8, '0')[::-1], 2))
        out = out[8:]
    return result