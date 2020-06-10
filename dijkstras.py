import numpy as np
def getPath(a,start,end,h):

    # i m takin 'a' output from shubham
    mat = a.reshape(1, 25)
    goal=end
    # start = int(input('type current location ie start point (0-24) and press enter:'))
    # goal = int(input('type target location and press enter:'))

    azk = 99
    sw = 99
    sg = 99
    if h == 'syg':
        sy = syg = 0
        cy = sr = cr = cyg = srg = crg = 1
    elif h == 'cyg':
        sy = 1
        cy = 0
        sr = 1
        cr = 1
        syg = 1
        cyg = 0
        srg = 1
        crg = 1
    elif h == 'srg':
        sy = 1
        cy = 1
        sr = 0
        cr = 1
        syg = 1
        cyg = 1
        srg = 0
        crg = 1
    elif h == 'crg':
        sy = 1
        cy = 1
        sr = 1
        cr = 0
        syg = 1
        cyg = 1
        srg = 1
        crg = 0
    else:
        sy = 0
        cy = 0
        sr = 0
        cr = 0
        syg = 1
        cyg = 1
        srg = 1
        crg = 1

    mat[mat == 1] = sr
    mat[mat == 2] = cr
    mat[mat == 3] = sy
    mat[mat == 4] = cy
    mat[mat == 5] = azk
    mat[mat == 6] = azk
    mat[mat == 7] = sw
    mat[mat == 8] = sw
    mat[mat == 9] = sg
    mat[mat == 10] = sg
    mat[mat == 11] = srg
    mat[mat == 12] = syg
    mat[mat == 13] = azk
    mat[mat == 14] = azk
    mat[mat == 15] = crg
    mat[mat == 16] = cyg
    mat[mat == 17] = azk
    mat[mat == 18] = azk

    mat = mat.reshape(5, 5)

    graph = {1: {2: mat[0][1], 6: mat[1][0]},
             2: {1: mat[0][0], 7: mat[1][1], 8: mat[0][2]},
             3: {2: mat[0][1], 4: mat[0][3], 8: mat[1][2]},
             4: {5: mat[0][4], 3: mat[0][2], 9: mat[1][3]},
             5: {4: mat[0][3], 10: mat[1][4]},
             6: {1: mat[0][0], 7: mat[1][1], 11: mat[2][0]},
             7: {2: mat[0][1], 6: mat[1][0], 12: mat[2][1], 8: mat[1][2]},
             8: {3: mat[0][2], 7: mat[1][1], 9: mat[1][3], 13: mat[2][2]},
             9: {4: mat[0][3], 8: mat[1][2], 10: mat[1][4], 14: mat[2][3]},
             10: {5: mat[0][4], 9: mat[1][3], 15: mat[2][4]},
             11: {6: mat[1][0], 12: mat[2][1], 16: mat[3][0]},
             12: {7: mat[1][1], 11: mat[2][0], 13: mat[2][2], 17: mat[3][1]},
             13: {8: mat[1][2], 12: mat[2][1], 14: mat[2][3], 18: mat[3][2]},
             14: {9: mat[1][3], 13: mat[2][2], 19: mat[3][3], 15: mat[2][4]},
             15: {10: mat[1][4], 14: mat[2][3], 20: mat[3][4]},
             16: {11: mat[2][0], 17: mat[3][1], 21: mat[4][0]},
             17: {12: mat[2][1], 16: mat[3][0], 18: mat[3][2], 22: mat[4][1]},
             18: {13: mat[2][2], 17: mat[3][1], 19: mat[3][3], 23: mat[4][2]},
             19: {14: mat[2][3], 18: mat[3][2], 24: mat[4][3], 20: mat[3][4]},
             20: {15: mat[2][4], 19: mat[3][3], 25: mat[4][4]},
             21: {16: mat[3][0], 22: mat[4][1]},
             22: {17: mat[3][1], 21: mat[4][0], 23: mat[4][2]},
             23: {18: mat[3][2], 22: mat[4][1], 24: mat[4][3]},
             24: {19: mat[3][3], 23: mat[4][2], 25: mat[4][4]},
             25: {20: mat[3][4], 24: mat[4][3]}}

    path = []

    def dijkstra(graph, start, goal):
        shortest_distance = {}
        predecessor = {}
        unseenNodes = graph
        infinity = 9999999

        for node in unseenNodes:
            shortest_distance[node] = infinity
        shortest_distance[start] = 0

        while unseenNodes:
            minNode = None
            for node in unseenNodes:
                if minNode is None:
                    minNode = node
                elif shortest_distance[node] < shortest_distance[minNode]:
                    minNode = node

            for childNode, weight in graph[minNode].items():
                if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                    shortest_distance[childNode] = weight + shortest_distance[minNode]
                    predecessor[childNode] = minNode
            unseenNodes.pop(minNode)

        currentNode = goal
        while currentNode != start:
            try:
                path.insert(0, currentNode)
                currentNode = predecessor[currentNode]
            except KeyError:
                print('Path not reachable or more than 1 route are equaly likely')
                break
        path.insert(0, start)
        if shortest_distance[goal] != infinity:
            print('Shortest distance is ' + str(shortest_distance[goal]))
            print('And the path is ' + str(path))

    dijkstra(graph, start, goal)
    return path

# getPath(np.array([[ 7.,  1.,  2.,  1., 12.],
#  [ 2.,  1.,  4.,  2.,  3.],
#  [14.,  2.,  1.,  3.,  7.],
#  [ 4.,  3.,  3.,  3.,  7.],
#  [15.,  1.,  4.,  2., 13.]]),25,11,0)