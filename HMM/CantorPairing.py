import math

def pair(x, y):

    pair_index = int(((x*x + 3*x + 2*x*y + y + y*y) / 2))

    return pair_index

def un_pair(pair_index):
    i = math.floor((-1 + math.sqrt(1 + 8*pair_index)) / 2)
    x = int((pair_index - ((i*(1+i)) / 2)))
    y = int((((i*(3 + i)) / 2) - pair_index))

    return (x, y)

def main():
    pair_index = pair(1, 2)
    print(un_pair(pair_index))
    un_pair(pair_index)




if __name__ == "__main__":
    main()