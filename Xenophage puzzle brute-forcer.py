# Replace target and puzzle following this format:
#   target
# TL  TM  TR
# ML   M  MR
# BL  BM  BR
# where V-symbol=0, A=1, X=2, horizontal bois=3. this is programming goddamnit, we start at 0.
# [TL,TM,TR,ML,M,MR,BL,BM,BR]
puzzle = [1, 1, 1, 1, 1, 1, 1, 1, 1]
target = 0

# Example puzzles and targets below:

# Archer's Line/K1 Logistics
#puzzle = [3,3,3,1,3,3,3,3,3]
#target = 1

# Anchor of Light/K1 Communion
#puzzle = [1,2,1,3,2,3,2,0,2]
#target = 0

# Hellmouth/K1 Crew Quarters
#puzzle = [1,2,0,1,2,2,1,1,1]
#target = 3

# Sorrow's Harbor/K1 Revelation
#puzzle = [3,1,0,0,2,0,3,1,0]
#target = 2

# -------------------------------------------------
# Don't need to edit anything past these lines.
# -------------------------------------------------

debug = False

from collections import deque

m = [[1, 1, 1, 1, 0, 0, 1, 0, 0], [1, 1, 1, 0, 1, 0, 0, 1, 0],
     [1, 1, 1, 0, 0, 1, 0, 0, 1], [1, 0, 0, 1, 1, 1, 1, 0, 0],
     [0, 1, 0, 1, 1, 1, 0, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0, 1],
     [1, 0, 0, 1, 0, 0, 1, 1, 1], [0, 1, 0, 0, 1, 0, 1, 1, 1],
     [0, 0, 1, 0, 0, 1, 1, 1, 1]]


def hash4(arr):
    return arr[0] + 4 * arr[1] + 16 * arr[2] + 64 * arr[3] + 256 * arr[
        4] + 1024 * arr[5] + 4096 * arr[6] + 16384 * arr[7] + 65536 * arr[8]


names = ["TL", "TM", "TR", "ML", "M", "MR", "BL", "BM", "BR"]


def solve(puzzle, target):
    maxd = 0
    solved = -1
    checked = {}
    queue = deque([[puzzle, [0, 0, 0, 0, 0, 0, 0, 0, 0], 0, 0]])
    answers = []
    while queue:
        [c, h, d, n] = queue.popleft()
        if solved > -1 and d > solved:
            return answers
        if d > maxd:
            maxd = d
            print "Checking depth: ", maxd

        # Check solution.
        doneA = True
        doneB = True
        first = c[0]
        for x in c:
            if x != first:
                doneA = False
            if x != target:
                doneB = False

        if doneB:
            if solved == -1:
                solved = d
            answers.append(h)

        if doneA and not doneB and debug:
            print "All " + str(c[0]) + "s, " + str(h)

        # Shoot symbol(s).
        for x in range(9):
            move = h[:]
            move[x] = move[x] + 1
            if move[x] > 3:
                continue
            latest = c[:]
            z = 0
            for y in m[x]:
                latest[z] = (latest[z] + y) % 4
                z = z + 1
            n = hash4(move)
            if n not in checked:
                queue.append([latest, move, d + 1, n])
                checked[n] = True

    # No solution.
    return []


answers = solve(puzzle, target)

if len(answers) > 0:
    # Sort by number of symbol positions to shoot.
    answers.sort(key=lambda moves: sum([not not count for count in moves]))

    count = 0
    for moves in answers:
        pretty = "{"
        sep = ""
        for x in range(9):
            if moves[x] > 0:
                pretty += sep
                sep = ", "
            if moves[x] == 1:
                pretty += names[x]
            elif moves[x] > 1:
                pretty += names[x] + "x" + str(moves[x])
        pretty += "}"
        count += 1
        print "Solution #{} found:".format(count), pretty

    if count > 1:
        print "Any of the above solutions will work."
    print "Solution format is some combination of [Top,Mid,Bottom]x[Left,Mid,Right]x[Count]."
else:
    print "No solutions found."
