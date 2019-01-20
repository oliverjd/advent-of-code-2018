# Advent of Code 2018 - Day 15
# Solution by Oliver Dunkley (https://dunkley.me)

from collections import deque


class Board(object):
    def __init__(self, bootstrap, elf_power=3):
        self.X = len(bootstrap[0])
        self.Y = len(bootstrap)
        self.board = [[None for _ in range(self.X)] for _ in range(self.Y)]
        for y in range(self.Y):
            for x in range(self.X):
                if bootstrap[y][x] == '#':
                    self.board[y][x] = Wall()
                elif bootstrap[y][x] in ['E', 'G']:
                    self.board[y][x] = Player(bootstrap[y][x], x, y, elf_power)

    def serialise(self):
        for y in range(self.Y):
            row = ''
            for x in range(self.X):
                if not self.board[y][x]:
                    row += '.'
                elif type(self.board[y][x]) == Wall:
                    row += '#'
                elif type(self.board[y][x]) == Player:
                    row += self.board[y][x].team
            print(row)
        print('')


class Wall(object):
    def __init__(self):
        pass


class Player(object):
    def __init__(self, team, x, y, elf_power):
        self.team = team
        self.health = 200
        self.attack = elf_power if team == 'E' else 3
        self.x = x
        self.y = y


def is_valid(x, y, xn, yn, board, visited):
    if 0 <= xn < board.X and 0 <= yn < board.Y:
        if (x, y, xn, yn) not in visited and not board.board[yn][xn]:
            return True
    return False


def shortest_path(player_x, player_y, x, y, board):
    queue = deque()
    queue.append((player_x, player_y, 0, []))
    first_moves = []
    visited_set = set()

    min_dist = 1000000000

    while len(queue) > 0:
        (n_x, n_y, n_d, n_p) = queue.popleft()

        if n_x == x and n_y == y:
            if n_d < min_dist:
                first_moves = [(n_p[0][0], n_p[0][1])]
                min_dist = n_d
            elif n_d == min_dist:
                first_moves.append((n_p[0][0], n_p[0][1]))
            continue

        if is_valid(n_x, n_y, n_x, n_y - 1, board, visited_set):
            visited_set.add((n_x, n_y, n_x, n_y-1))
            queue.append((n_x, n_y - 1, n_d + 1, n_p + [(n_x, n_y - 1)]))
        if is_valid(n_x, n_y, n_x - 1, n_y, board, visited_set):
            visited_set.add((n_x, n_y, n_x-1, n_y))
            queue.append((n_x - 1, n_y, n_d + 1, n_p + [(n_x - 1, n_y)]))
        if is_valid(n_x, n_y, n_x + 1, n_y, board, visited_set):
            visited_set.add((n_x, n_y, n_x+1, n_y))
            queue.append((n_x + 1, n_y, n_d + 1, n_p + [(n_x + 1, n_y)]))
        if is_valid(n_x, n_y, n_x, n_y + 1, board, visited_set):
            visited_set.add((n_x, n_y, n_x, n_y+1))
            queue.append((n_x, n_y + 1, n_d + 1, n_p + [(n_x, n_y + 1)]))

    # changing the order of the above 4 'if's changes the behaviour of the outcome which it shouldn't if we are actually
    # exploring every path... however, as long as we only care about the path with the first move in reading order and
    # nothing else even though this is technically an incorrect bfs that doesn't explore all possible paths, it works.

    if min_dist != 1000000000:
        first_move = (None, None)
        for move in first_moves:
            if not first_move[0]:
                first_move = move
            elif move[1] < first_move[1]:
                first_move = move
            elif move[1] == first_move[1] and move[0] < first_move[0]:
                first_move = move
        return min_dist, first_move
    else:
        return -1, None


def attack_if_possible(board, player, alive_E, alive_G):
    attackable = []
    if type(board.board[player.y][player.x + 1]) == Player and board.board[player.y][player.x + 1].team != player.team:
        attackable.append(board.board[player.y][player.x + 1])
    if type(board.board[player.y][player.x - 1]) == Player and board.board[player.y][player.x - 1].team != player.team:
        attackable.append(board.board[player.y][player.x - 1])
    if type(board.board[player.y + 1][player.x]) == Player and board.board[player.y + 1][player.x].team != player.team:
        attackable.append(board.board[player.y + 1][player.x])
    if type(board.board[player.y - 1][player.x]) == Player and board.board[player.y - 1][player.x].team != player.team:
        attackable.append(board.board[player.y - 1][player.x])
    if len(attackable) > 0:
        to_attack = None
        lowest_health = 1000
        for a in attackable:
            if a.health < lowest_health:
                lowest_health = a.health
                to_attack = a
            elif a.health == lowest_health:
                if a.y < to_attack.y:
                    to_attack = a
                elif a.y == to_attack.y and a.x < to_attack.x:
                    to_attack = a
        to_attack.health -= player.attack
        if to_attack.health <= 0:
            board.board[to_attack.y][to_attack.x] = None
            if to_attack.team == 'E':
                alive_E.remove(to_attack)
            else:
                alive_G.remove(to_attack)
        return True
    return False


def turn(board):
    player_order = []
    alive_E = set()
    alive_G = set()
    for y in range(board.Y):
        for x in range(board.X):
            if type(board.board[y][x]) == Player:
                player_order.append(board.board[y][x])
                if board.board[y][x].team == 'E':
                    alive_E.add(board.board[y][x])
                else:
                    alive_G.add(board.board[y][x])
    for player in player_order:
        if player.health <= 0:
            continue
        if (player.team == 'E' and len(alive_G) == 0) or (player.team == 'G' and len(alive_E) == 0):
            return True
        targets = alive_G if player.team == 'E' else alive_E
        if attack_if_possible(board, player, alive_E, alive_G):
            continue
        in_range = []
        for enemy in targets:
            if not board.board[enemy.y][enemy.x + 1]:
                in_range.append((enemy.x + 1, enemy.y))
            if not board.board[enemy.y][enemy.x - 1]:
                in_range.append((enemy.x - 1, enemy.y))
            if not board.board[enemy.y + 1][enemy.x]:
                in_range.append((enemy.x, enemy.y + 1))
            if not board.board[enemy.y - 1][enemy.x]:
                in_range.append((enemy.x, enemy.y - 1))
        reachable = []
        for pos in in_range:
            dist, first_move = shortest_path(player.x, player.y, pos[0], pos[1], board)
            if dist > -1:
                reachable.append({"target_square": pos, "dist": dist, "first_move": first_move})
        nearest = []
        if len(reachable) > 0:
            shortest_dist = min([x['dist'] for x in reachable])
            chosen_move = (None, None)
            target_to_choose = (None, None)
            for row in reachable:
                if row['dist'] == shortest_dist:
                    nearest.append({'first_move': row['first_move'], 'target_square': row['target_square']})
            for move in nearest:
                if not target_to_choose[0]:
                    chosen_move = move['first_move']
                    target_to_choose = move['target_square']
                elif move['target_square'][1] < target_to_choose[1]:
                    chosen_move = move['first_move']
                    target_to_choose = move['target_square']
                elif move['target_square'][1] == target_to_choose[1] and move['target_square'][0] < target_to_choose[0]:
                    chosen_move = move['first_move']
                    target_to_choose = move['target_square']
            board.board[player.y][player.x] = None
            player.x = chosen_move[0]
            player.y = chosen_move[1]
            board.board[player.y][player.x] = player
            if attack_if_possible(board, player, alive_E, alive_G):
                continue


def part_1(input):
    in_list = [x.strip() for x in list(input)]
    board = Board(in_list)

    done = None
    i = -1
    while not done:
        i += 1
        done = turn(board)

    num_rounds = i
    hp_sum = 0
    for y in range(board.Y):
        for x in range(board.X):
            if type(board.board[y][x]) == Player:
                hp_sum += board.board[y][x].health

    return num_rounds * hp_sum


def part_2(input):
    in_list = [x.strip() for x in list(input)]

    elf_power = 3
    board = Board(in_list, elf_power)
    start_elves = sum([sum([1 for x in range(board.X) if type(board.board[y][x]) == Player
                            and board.board[y][x].team == 'E']) for y in range(board.Y)])

    while True:
        elf_power += 1
        board = Board(in_list, elf_power)
        done = None
        i = -1
        while not done:
            i += 1
            done = turn(board)

        count_elves = sum([sum([1 for x in range(board.X) if type(board.board[y][x]) == Player
                                and board.board[y][x].team == 'E']) for y in range(board.Y)])

        num_rounds = i
        hp_sum = 0
        for y in range(board.Y):
            for x in range(board.X):
                if type(board.board[y][x]) == Player:
                    hp_sum += board.board[y][x].health

        if count_elves == start_elves:
            break

    return num_rounds * hp_sum


if __name__ == "__main__":
    with open("../input/day_15.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
