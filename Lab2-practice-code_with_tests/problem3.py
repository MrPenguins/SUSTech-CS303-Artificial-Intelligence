"""
Example:
input:
map:
---------
------x--
-x-------
---@-----
---##----
------x--
--x----x-
-x-------
---------
action:
0 0 3 3 0 3 3 1 1 1 1 1 3 1 1 2 2 2 2 2

output:
7 3

"""

if __name__ == '__main__':
    test_case = 4
    with open(f'test_cases/problem3/{test_case}-map.txt', 'r') as f:
        game_map = [list(line.strip()) for line in f.readlines()]
    # print(game_map)
    with open(f'./test_cases/problem3/{test_case}-actions.txt', 'r') as f:
        actions = [*map(int, f.read().split(' '))]
    # print(actions)
