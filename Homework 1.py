

import numpy as np

# This is answer manual for homework 1.
#Columbia University
#Artificial Intelligences
#Dongbing Han / UNI: dh3071
#2021.9.2

def factorial(n):
    fac = 1
    for i in range(1, n+1):
        fac = fac * i

    return fac


def p1(k: int) -> str:
    string1=" "
    while (k > 1):
        string1 = string1 + str(factorial(k)) + ","
        k = k-1
    string1 = string1 + "1"
    return string1
    pass



def p2_a(x: list, y: list) -> list:
    newlst = sorted(y, reverse=True)
    newlst.pop()
    return newlst


def p2_b(x: list, y: list) -> list:
    newlst = x[::-1]
    return newlst
    pass


def p2_c(x: list, y: list) -> list:
    newlist = sorted(np.unique(x+y))
    return newlist
    pass


def p2_d(x: list, y: list) -> list:
    newlist = [x,y]
    return newlist
    pass


def p3_a(x: set, y: set, z: set) -> set:
    newset = x.union(y,z)
    return newset
    pass


def p3_b(x: set, y: set, z: set) -> set:
    newset = x.intersection(y,z)
    return newset
    pass


def p3_c(x: set, y: set, z: set) -> set:
    temp1 = x.union(y,z)
    temp2 = x.intersection(y)
    temp3 = x.intersection(z)
    temp4 = y.intersection(z)
    newset = temp1 -temp2 - temp3 - temp4
    return newset
    pass


def p4_a() -> np.array:
    a = np.array([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 2, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]])
    return a
    pass


def p4_b(x: np.array) -> list:
    #find the element 2
    newlst = []
    elerow = 0
    elecol = 0
    for i in range(len(x)):
        for j in range(len(x[i])):
           if (x[i][j] == 2):
               elerow = i
               elecol = j

    for ni in range (len(x)):
        for nj in range(len(x[ni])):
                if(x[ni][nj] == 1):

                    if (elerow - 1) >= 0:
                        if (ni == elerow - 1):
                            if (elecol - 2) >= 0:
                                if (nj == elecol - 2):
                                    newlst.append((ni, nj))
                            if (elecol + 2) < len(x):
                                if (nj == elecol + 2):
                                    newlst.append((ni, nj))

                    if (elerow + 1) < len(x):
                        if (ni == elerow + 1):
                            if (elecol - 2) >= 0:
                                if (nj == elecol - 2):
                                    newlst.append((ni, nj))
                            if (elecol + 2) < len(x):
                                if (nj == elecol + 2):
                                    newlst.append((ni, nj))



                    if (elerow - 2) >= 0:
                        if (ni == elerow - 2):
                            if (elecol - 1) >= 0:
                                if (nj == elecol - 1):
                                    newlst.append((ni, nj))
                            if (elecol + 1) < len(x):
                                if (nj == elecol + 1):
                                    newlst.append((ni,nj))

                    if (elerow + 2) < len(x):
                        if (ni == elerow + 2):
                            if (elecol - 1) >= 0:
                                if (nj == elecol - 1):
                                    newlst.append((ni, nj))
                            if (elecol + 1) < len(x):
                                if (nj == elecol + 1):
                                    newlst.append((ni,nj))

    return newlst
    pass


def p5_a(x: dict) -> int:
    track  = 0
    for value in x.values():
        if value == []:
            track = track +1
    return track
    pass


def p5_b(x: dict) -> int:
    track = 0
    for value in x.values():
        if value != []:
            track = track +1
    return track
    pass


def p5_c(x: dict) -> list:
    curtuple = ()
    for key in x.keys():
        for value in x[key]:
            if contains(curtuple, key, value) == False:
               y=list(curtuple)
               y.append((key,value))
               curtuple = tuple(y)

    return list(curtuple)
    pass

def contains(curtuple: list, key: str, value: str) -> bool:
    if curtuple.count((value,key)) == 0:
        return False
    else:
        return True


def p5_d(x: dict) -> np.array:
    length = len(x.keys())
    matrix = np.zeros([length, length], dtype = int)
    traverse = []

    for key in x.keys():
        if key not in traverse:
            traverse.append(key)

    for key in x.keys():
        for value in x[key]:
            matrix[traverse.index(key)][traverse.index(value)] = 1
    return matrix
    pass


class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        pass

    def push(self, x):
        self.queue.append(x)
        pass

    def pop(self):
        dirct = {'apple': 5.0, 'banana': 4.5, 'carrot': 3.3, 'kiwi': 7.4, 'orange': 5.0, 'mango': 9.1, 'pineapple': 9.1}
        try:
            max = 0
            track = 0
            for i in range(len(self.queue)):
                curk = self.queue[i]
                curv = dirct[curk]
                if  curv > track:
                    track = curv
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()


    def is_empty(self):
        return len(self.queue) == 0
        pass


if __name__ == '__main__':
    print(p1(k=8))
    print('-----------------------------')
    print(p2_a(x=[], y=[1, 3, 5]))
    print(p2_b(x=[2, 4, 6], y=[]))
    print(p2_c(x=[1, 3, 5, 7], y=[1, 2, 5, 6]))
    print(p2_d(x=[1, 3, 5, 7], y=[1, 2, 5, 6]))
    print('------------------------------')
    print(p3_a(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print(p3_b(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print(p3_c(x={1, 3, 5, 7}, y={1, 2, 5, 6}, z={7, 8, 9, 1}))
    print('------------------------------')
    print(p4_a())
    print(p4_b(p4_a()))
    print('------------------------------')
    graph = {
         'A': ['D', 'E'],
         'B': ['E', 'F'],
         'C': ['E'],
         'D': ['A', 'E'],
         'E': ['A', 'B', 'C', 'D'],
         'F': ['B'],
         'G': []
    }
    print(p5_a(graph))
    print(p5_b(graph))
    print(p5_c(graph))
    print(p5_d(graph))
    print('------------------------------')
    pq = PriorityQueue()
    pq.push('apple')
    pq.push('kiwi')
    pq.push('orange')
    while not pq.is_empty():
        print(pq.pop())