
class state():
    def __init__(self, array, parent,goal_board):
        self.board_size = 3
        self.arr = array
        self.parent = parent
        self.move = None
        self.depth = 0
        if self.parent:
            self.depth = parent.depth + 1

        self.goal_board = goal_board
        #self.estimated_cost = self.depth + self.__h()  # f = cost + h
        self.estimated_cost = self.__h()  # f = h


    def printBoard(self):
        for row in self.arr:
            print(row)
        print()

    def returnBoard(self):
        s = ""
        for row in self.arr:
            s += row.__repr__()+"\n"
        return s

    def __eq__(self, other):
        """
        this method was created in order to make the objects
        hashable so we can store them in a set
        """
        h1 = [item for row in self.arr for item in row]
        h2 = [item for row in other.arr for item in row]

        for i in range(self.board_size * self.board_size):
            if h1[i] != h2[i]:
                return False
        return True

    def children(self):
        """
        this method returns a list containing all the possible changes
        for the current state
        """
        n = []
        zi = 0
        zj = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.arr[i][j] == 0:
                    zi = i
                    zj = j
                    break
        i = zi
        j = zj
        # "UDLR" order; that is, [‘Up’, ‘Down’, ‘Left’, ‘Right’]
        if 0 <= i-1:  # up
            self.arr[i][j], self.arr[i-1][j] = self.arr[i -
                                                        1][j], self.arr[i][j]  # do the move
            x = state([row[:] for row in self.arr],
                      self,self.goal_board)  # create a copy
            x.move = "Up"  # set the movement that leads for this copy
            n.append(x)  # add the copy to the list
            # undo the move so we can continue finding the other children
            self.arr[i][j], self.arr[i-1][j] = self.arr[i-1][j], self.arr[i][j]
        if self.board_size > i+1 :  # down
            self.arr[i][j], self.arr[i+1][j] = self.arr[i+1][j], self.arr[i][j]
            x = state([row[:] for row in self.arr], self,self.goal_board)
            x.move = "Down"
            n.append(x)
            self.arr[i][j], self.arr[i+1][j] = self.arr[i+1][j], self.arr[i][j]
        if 0 <= j-1:  # left
            self.arr[i][j], self.arr[i][j-1] = self.arr[i][j-1], self.arr[i][j]
            x = state([row[:] for row in self.arr], self,self.goal_board)
            x.move = "Left"
            n.append(x)
            self.arr[i][j], self.arr[i][j-1] = self.arr[i][j-1], self.arr[i][j]
        if self.board_size > j+1:  # right
            self.arr[i][j], self.arr[i][j+1] = self.arr[i][j+1], self.arr[i][j]
            x = state([row[:] for row in self.arr], self,self.goal_board)
            x.move = "Right"
            n.append(x)
            self.arr[i][j], self.arr[i][j+1] = self.arr[i][j+1], self.arr[i][j]

        return n

    def bestChild(self):
        arr = self.children()
        best = arr[0]
        for i in range(1,len(arr)):
            if arr[i].estimated_cost < best.estimated_cost:
                best=arr[i]
        """
        for i in arr:
            print(i.estimated_cost)
        print("best : ", best.estimated_cost)
        print("me : " , self.estimated_cost)
        """
        return best

    def __h(self):  # _manhattan_distance
        """
        used for calulcating the estimated cost for reaching a the goal state from our current state
        """
        h2 = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                #print(self.arr)
                if self.arr[i][j] == 0:
                    continue
                for i2 in range(self.board_size):
                    for j2 in range(self.board_size):
                        if self.arr[i][j] == self.goal_board[i2][j2]:
                            h2 += abs(i2 - i) + abs(j2 - j)

        return h2

    def __repr__(self):
        return self.returnBoard()


def hillClimbing(initialState):
    currentSolution = initialState
    currentRouteLength = currentSolution.estimated_cost
    #print("Current Solution:", currentSolution, "Route Length: ", currentRouteLength)
    bestNeighbour = initialState.bestChild()

    while bestNeighbour.estimated_cost < currentRouteLength:
        currentSolution = bestNeighbour
        currentRouteLength = bestNeighbour.estimated_cost
        #print("Current Solution: ", currentSolution, "  Route Length: ", currentRouteLength)
        bestNeighbour = currentSolution.bestChild()

    return currentSolution

def main():
    #for the normal running of the program
    """
    sarr=[[2,1,5],
           [6,0,4],
           [3,7,8]]

    garr=[[1,2,3],
           [4,5,6],
           [7,8,0]]
    """
    sarr=[[7,1,5],
           [8,0,4],
           [3,2,6]]

    garr=[[1,2,3],
           [4,5,6],
           [7,8,0]]

    
    s = state(sarr, None,garr)
    g = state(garr, None,garr)

    print("The initial state :")
    print(s)
    print("The goal state :")
    print(g)

    ans = hillClimbing(s)
    h = ans
    path = []
    while h.move != None:
        path.append(h.move)
        h = h.parent
    path.reverse()
    
    print("path", path)
    print("The best possible reached state :")
    print(ans)
    print("The best possible reached cost : ",ans.estimated_cost)
    
    
    #///////////////////////////////////////////////////////////
    
    return

if __name__ == "__main__":
    main()
