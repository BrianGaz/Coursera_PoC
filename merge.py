"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    setup_line = line[:]
    new_line = []
    for num in setup_line:
        if num == 0:
            setup_line.remove(0)
            setup_line.append(0)
            
    setup_line.append(0)
    setup_line.append(0)
    setup_line.append(0)
    setup_line.append(0)
    
    for itr in range(len(line)):
        print setup_line
        print new_line
        if setup_line[0] == setup_line[1] and setup_line[0] != 0:
            new_line.append(setup_line[0] * 2)
            setup_line.remove(setup_line[0])
            setup_line.remove(setup_line[0])
        else:
            new_line.append(setup_line[0])
            setup_line.remove(setup_line[0])
    new_line.append(0)
    
    for itr in range(len(new_line)):
        for num in new_line[len(line):]:
            if num == 0:
                new_line.remove(0)
    
    return new_line

print merge([2,2,8,8,4,4])
