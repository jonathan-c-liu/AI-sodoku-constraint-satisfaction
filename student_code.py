import common

#helpful, but not needed
class variables:
	counter=0


def sudoku_backtracking(sudoku):
	variables.counter = 0
	recursive_backtracking(sudoku)
	return variables.counter

def recursive_backtracking(sudoku):
	variables.counter += 1
	square = None
	for y in range(9):
		for x in range(9):
			if sudoku[y][x] == 0 and not square:
				square = (y, x)
	if not square:
		return True
	for v in range(1, 10):
		if common.can_yx_be_z(sudoku, square[0], square[1], v):
			sudoku[square[0]][square[1]] = v
			if recursive_backtracking(sudoku):
				return True
			else:
				sudoku[square[0]][square[1]] = 0

def sudoku_forwardchecking(sudoku):
	variables.counter = 0
	domain = [[[0 for x in range(9)] for x in range(9)] for x in range(9)]
	for y in range(9):
		for x in range(9):
			for v in range(1, 10):
				if common.can_yx_be_z(sudoku, y, x, v):
					domain[y][x][v - 1] = 1
	recursive_forwardchecking(sudoku, domain)
	return variables.counter

def recursive_forwardchecking(sudoku, domain):
	variables.counter += 1
	square = None
	for y in range(9):
		for x in range(9):
			if sudoku[y][x] == 0 and not square:
				square = (y, x)
	if not square:
		return True
	for v in range(1, 10):
		if common.can_yx_be_z(sudoku, square[0], square[1], v):
			old_domain = mycopy(domain)
			sudoku[square[0]][square[1]] = v
			if update_domain(domain, sudoku, square, v):
				if recursive_forwardchecking(sudoku, domain):
					return True
			sudoku[square[0]][square[1]] = 0
			domain = mycopy(old_domain)


def update_domain(domain, sudoku, square, v):
	squares = []
	for i in range(9):
		squares.append((square[0], i))
		squares.append((i, square[1]))
		squares.append((int(square[0] / 3) * 3 + int(i / 3), int(square[1] / 3) * 3 + i % 3))
	squares = list(dict.fromkeys(squares))
	for s in squares:
		if sudoku[s[0]][s[1]] == 0:
			domain[s[0]][s[1]][v - 1] = 0
			if sum(domain[s[0]][s[1]]) == 0:
				return False
	return True


def mycopy(original):
	copy = [[[0 for x in range(9)] for x in range(9)] for x in range(9)]
	for i in range(9):
		for j in range(9):
			for k in range(9):
				copy[i][j][k] = original[i][j][k]
	return copy