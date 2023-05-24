from queue import Queue
import copy
import numpy as np

class node(object):
    # constructor method
    def __init__(self, state, parent):
        self.state = copy.deepcopy(state)
        self.parent = parent
        self.children = []

    def terminal(self):
        """
        Returns True if game is over, False otherwise.
        """
        for row in self.state:
            for cell in row:
                if cell == 0:
                    return False
        return True

    
    def find_possible_moves(self):

        nodes = []
        # for getting all the possible slots to be filled
        i = 0
        j = 0
        slots = set()
        board = self.state
        for row in board:
            j = 0
            for cell in row:
                if cell == 0:
                    slots.add((i, j))
                j += 1
            i += 1
        for slot in slots:
            x = slot[0]
            y = slot[1]
            nvalid = 0
            for n in range(1, 10):
                #check if the value didn't occur in the vertical line
                skip = False
                for m in range(0, 9):
                    if board[m][y] == n:
                        skip = True
                        break

                if not skip:
                    #check if the value didn't occur in the horizontal line
                    for m in range(0, 9):
                        if board[x][m] == n:
                            skip = True
                            break                
                        
                if not skip:
                    #check if the value didn't occur in the 3x3 grid of the cell
                    if x < 3:      
                        strt_row = 0
                        end_row = 3
                    elif x >= 3 and x < 6:
                        strt_row = 3
                        end_row = 6
                    else:                 
                        strt_row = 6
                        end_row = 9   
                        
                    if y < 3:
                        strt_col= 0
                        end_col = 3                        
                    elif y >= 3 and y < 6:
                        strt_col= 3
                        end_col = 6  
                    else:
                        strt_col= 6
                        end_col = 9

                    sub_board = board[strt_row:end_row, strt_col:end_col]
                    for row in sub_board:
                        for cell in row:
                            if cell == n:
                                skip = True
                                break

                if not skip:
                    nvalid += 1
                    child = node(board, self)
                    # filling the empty cell with the valid value for the child
                    child.state[x][y] = n
                    nodes.append(child)
                
                # stop at two feasible values per cell
                if nvalid > 1:
                    break
            # return the only valid value for a cell if existed
            if nvalid == 1:
                return nodes[-1:]

        # return all the possible values for the empty cells in the initial state
        if self.parent == None:
            return nodes[:len(nodes)//2]
        else:
            return nodes[-1:]

    def check_initial_state(self):

        board = copy.deepcopy(self.state)
        # check duplicate values in columns or rows
        for x in range(9):
            sub_board = board[:,x]
            u, c = np.unique(sub_board, return_counts=True)
            dup = u[c > 1]
            if 0 not in dup and len(dup) > 0:
                return False            
            sub_board = board[x,:]
            u, c = np.unique(sub_board, return_counts=True)
            dup = u[c > 1]
            if 0 not in dup and len(dup) > 0:
                return False


        #check if the value didn't occur in the 3x3 grid of the cell
        inds = [0, 3, 6, 9]
        for x in range(3):
            for y in range(3):
                sub_board = board[inds[x]:inds[x+1],inds[y]:inds[y+1]]
                u, c = np.unique(sub_board, return_counts=True)
                dup = u[c > 1]
                if 0 not in dup and len(dup) > 0:
                    return False
        return True

    def find_children(self):
        nodes = self.find_possible_moves()
        for elem in nodes:
            self.children.append(elem)
    
def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    # initial state node
    initial_node = node(sudoku, None)
    # checking initial state
    valid = initial_node.check_initial_state()
    if not valid:
        return np.full((9, 9), -1)

    queue = Queue()
    queue.put(initial_node)
 
    while (not queue.empty()):
        current_node = queue.get()
        # checking if the game is ended
        done = current_node.terminal()
        if done:
            solved_sudoku = current_node.state
            return solved_sudoku

        # getting all the possible moves from the current state
        current_node.find_children()

        # adding all the possible moves to the queue
        for child in current_node.children:
                queue.put(child)
   
    # returning np array with values of -1 in case no solution is found
    return np.full((9, 9), -1)


if __name__ == '__main__':
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = np.load(f"{difficulty}_puzzle.npy")
        solutions = np.load(f"{difficulty}_solution.npy")
        
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)
            
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)
            
            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
            
            print("This sudoku took", end_time-start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break
