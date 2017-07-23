assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def concat(A,B):
    con = []
    assert len(A) == len(B)
    for i in range(len(A)):
        conx = A[i-1] + B[i-1]
        con.append(conx)
    return con

boxes = [s+t for s in 'ABCDEFGHI' for t in '123456789']
rows = 'ABCDEFGHI'
cols = '123456789'
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [concat(rows,cols),concat(rows[::-1],cols)]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Step1: mapping key 1 over its corresponding units (row unit/ column unit/ square unit/ squart unit) to identify twins
    # Step2: if the count of successful mapping is greater than or equal to 2, replace 2 figures with "" in all its corresponding units and not to remove the twins themselves

    for key1 in values.keys():
        for unit in units[key1]:
            count = 0 # Counter starts again for each unit (row unit/ column unit/ square unit/ squart unit)
            for key2 in unit:       
                    if len(values[key1]) == 2 and len(values[key2]) == 2:
                        if values[key1]== values[key2]:
                            count += 1

            if count >= 2:
                for peer in unit:
                    if values[peer] != values[key1] and len(values[peer])>1: # not to exclude the twins themselves
                        assign_value(values, peer, values[peer].replace(values[key1][0],''))
                        assign_value(values, peer, values[peer].replace(values[key1][1],''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    string = []
    for c in grid:
    	if c == ".":
    		string.append('123456789')
    	else:
    		string.append(c)
    return dict(zip(boxes,string))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    # Copy from Util
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solvedkeys = []
    for c in values.keys():
        if len(values[c]) == 1:
            solvedkeys.append(c) 
    
    for c in solvedkeys:
        figure = values[c] # Call the solved value
        for peer in peers[c]: # Loop through each corresponding peer and replace the solved value that with ""
            values[peer] = values[peer].replace(figure,"")
            
    return values

def only_choice(values):
    for unit in unitlist:
        for i in "123456789":
            matchedcell = [] # Count for each digit and each unitlist
            for u in unit:
                if i in values[u]:
                    matchedcell.append(u)
            if len(matchedcell)==1:
                values[matchedcell[0]]= i
    return values

def reduce_puzzle(values):
    Vain = False
    while not Vain:
        before = len([box for box in values.keys() if len(values[box])==1])
        eliminate(values)
        only_choice(values)
        naked_twins(values)
        after = len([box for box in values.keys() if len(values[box])==1])
        if before == after:
            Vain = True
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values   

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ##Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    else:
        n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
        # Now use recurrence to solve each one of the resulting sudokus, and 
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku[s] = value
            attempt = search(new_sudoku)
            if attempt:
                return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
