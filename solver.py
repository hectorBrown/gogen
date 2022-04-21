def get_locs(letter):
    output = []
    for y in range(len(map)):
        for x in range(len(map[0])):
            if letter in map[y][x]:
                output.append((y, x))
    return output
def get_surrounding(loc):
    output = []
    for x_scan in range(-1, 2):
        for y_scan in range(-1, 2):
            output_pt = (loc[0] + y_scan, loc[1] + x_scan)
            if all([x >= 0 and x < len(map) for x in output_pt]) and not (x_scan == 0 and y_scan == 0):
                output.append(output_pt)
    return output

#load
words = [x.replace("\n", "") for x in open("words").readlines()]
exc = open("except").readline()
alph = list(filter(lambda x : x != exc, [chr(i) for i in range(65, 65 + 26)]))
map = [[alph.copy() if c == "." else [c] for c in x.replace("\n", "")] for x in open("map").readlines()]

#init is list of initialising letters to cut down possibililities on first sweep
init = []
#just add to init those that we're already sure about
for y in range(len(map)):
    for x in range(len(map[0])):
        if len(map[y][x]) == 1:
            init.append(map[y][x][0])
#cut out init values
for y in range(len(map)):
    for x in range(len(map[0])):
        if len(map[y][x]) != 1:
            for letter in init:
                map[y][x].remove(letter)

filled = False
while not filled:
    #scroll over word list
    for word in words:
        #for each letter in the word
        for i, letter in enumerate(word):
            #find neighbouring letters in word (one away)
            neighbours = []
            if i - 1 >= 0:
                neighbours.append(word[i - 1])
            if i + 1 < len(word):
                neighbours.append(word[i + 1])
            #find positions of the letter
            locs = get_locs(letter)
            #find all locations that are one away from one of the letter locations
            neighbour_locs = []
            for loc in locs:
                surrounding = get_surrounding(loc)
                for pt in surrounding:
                    if not pt in neighbour_locs:
                        neighbour_locs.append(pt)
            #find all valid locations that aren't in neighbour_locs
            not_neighbour_locs = []
            for y in range(len(map)):
                for x in range(len(map[0])):
                    if (y, x) not in neighbour_locs:
                        not_neighbour_locs.append((y, x))
            #remove neighbouring letters from those positions
            for target in not_neighbour_locs:
                for neighbour in neighbours:
                    if neighbour in map[target[0]][target[1]]:
                        map[target[0]][target[1]].remove(neighbour)
    #trim all values that are completed
    completed = []
    for y in range(len(map)):
        for x in range(len(map[0])):
            if len(map[y][x]) == 1:
                completed.append(map[y][x][0])
    for y in range(len(map)):
        for x in range(len(map[0])):
            if len(map[y][x]) > 1:
                for letter in completed:
                    if letter in map[y][x]:
                        map[y][x].remove(letter)
    #check if grid finished
    filled = True
    for y in range(len(map)):
        for x in range(len(map[0])):
            if len(map[y][x]) > 1:
                filled = False

output = ""
for y in range(len(map)):
    for x in range(len(map[0])):
        output += map[y][x][0]
    output += "\n"
print(output)