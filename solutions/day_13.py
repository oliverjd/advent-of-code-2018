# Advent of Code 2018 - Day 13
# Solution by Oliver Dunkley (https://dunkley.me)


def run(input):
    """ A pretty horrible solution, but it works. Final cart is shown as the odd one out of the last three, after
    one more movement. """
    state = []
    for line in input:
        state.append(line.strip('\n'))

    track = []
    carts = []
    cart_id = 0
    for y in range(len(state)):
        row = ''
        for x in range(len(state[y])):
            if state[y][x] not in ('^', 'v', '<', '>'):
                row += state[y][x]
            else:
                carts.append([y, x, state[y][x], 'l', cart_id])
                cart_id += 1
                if state[y][x] in ('^', 'v'):
                    new = '|'
                elif state[y][x] in ('<', '>'):
                    new = '-'
                row += new
        track.append(row)

    print(carts)

    first_crash = None
    crashes = []
    done = False
    while not done:
        carts = sorted(carts, key=lambda k: [k[0], k[1]])
        print(carts)
        new_carts = []
        this_iter_crash_ids = []
        for cart in carts:
            if cart[4] in this_iter_crash_ids:
                carts.remove(cart)
                continue
            new_y = cart[0]
            new_x = cart[1]
            c = cart[2]
            new_c = c
            new_dir = cart[3]
            if c == '^':
                new_y -= 1
                if track[new_y][new_x] == '+':
                    # turn
                    if cart[3] == 'l':
                        new_dir = 's'
                        new_c = '<'
                    elif cart[3] == 'r':
                        new_dir = 'l'
                        new_c = '>'
                    else:
                        new_dir = 'r'
                elif track[new_y][new_x] == '\\':
                    new_c = '<'
                elif track[new_y][new_x] == '/':
                    new_c = '>'
            elif c == 'v':
                new_y += 1
                if track[new_y][new_x] == '+':
                    if cart[3] == 'l':
                        new_dir = 's'
                        new_c = '>'
                    elif cart[3] == 'r':
                        new_dir = 'l'
                        new_c = '<'
                    else:
                        new_dir = 'r'
                elif track[new_y][new_x] == '/':
                    new_c = '<'
                elif track[new_y][new_x] == '\\':
                    new_c = '>'
            elif c == '>':
                new_x += 1
                if track[new_y][new_x] == '+':
                    if cart[3] == 'l':
                        new_dir = 's'
                        new_c = '^'
                    elif cart[3] == 'r':
                        new_dir = 'l'
                        new_c = 'v'
                    else:
                        new_dir = 'r'
                elif track[new_y][new_x] == '/':
                    new_c = '^'
                elif track[new_y][new_x] == '\\':
                    new_c = 'v'
            elif c == '<':
                new_x -= 1
                if track[new_y][new_x] == '+':
                    if cart[3] == 'l':
                        new_dir = 's'
                        new_c = 'v'
                    elif cart[3] == 'r':
                        new_dir = 'l'
                        new_c = '^'
                    else:
                        new_dir = 'r'
                elif track[new_y][new_x] == '/':
                    new_c = 'v'
                elif track[new_y][new_x] == '\\':
                    new_c = '^'
            new_cart = [new_y, new_x, new_c, new_dir, cart[4]]
            this_cart_crashed = False
            for c2 in new_carts:
                if c2[0] == new_y and c2[1] == new_x:
                    if not first_crash:
                        first_crash = [new_x, new_y]
                    crashes.append([new_y, new_x])
                    this_cart_crashed = True
                    this_iter_crash_ids.append(c2[4])
            for c2 in carts:
                if c2[0] == new_y and c2[1] == new_x:
                    if c2[4] != cart[4]:
                        if not first_crash:
                            first_crash = [new_x, new_y]
                        crashes.append([new_y, new_x])
                        this_cart_crashed = True
                        this_iter_crash_ids.append(c2[4])
            if not this_cart_crashed:
                new_carts.append(new_cart)
            for crashed in this_iter_crash_ids:
                for c in new_carts:
                    if c[4] == crashed:
                        new_carts.remove(c)
        carts = new_carts
        if len(carts) < 1:
            done = True

    return first_crash


if __name__ == "__main__":
    with open("../input/day_13.txt") as f:
        print(run(f))
