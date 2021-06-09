"""
SOLVES THE https://wiki.guildwars2.com/wiki/%22Where%27s_Balthazar%22 PUZZLE IN S3E6

In case you f'ed up and have different state than wiki has
I recommend you to always look to puzzle from south towards north

run with S3E6_puzzle_solver.py --file state
where state is file with puzzle state

        NORTH

WEST    101      EAST
        1-0
        101

        SOUTH

File should contain matrix 3x3 where
0 means puzzle piece is not LIT
1 means puzzle piece is LIT
- means center of puzzle

Example file:

101
0-0
000

If puzzle has no solutions (case of input being wrong), program will result in "No solutions" message
If puzzle has exactly one solution, it is printed
If puzzle has two and more solutions, you can choose by order found

Solution is printed as action needed to move from initial to target state
Left part means row
Right part means column

ROWS:
    First row = TOP
    Second row = CENTER
    Third row = BOTTOM
    
COLUMNS:
    First column = LEFT
    Second column = CENTER
    Third column = RIGHT
    
Example: CENTER RIGHT means second row and third column
And similar

Code is bad but should give result
Made by Sognus.1204
"""



import argparse
import traceback
import numpy as np
import pprint


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", dest="file", help="Name of file with state", required=True)
    return parser.parse_args()


class State:

    def __init__(self, data=None, filename=None):
        self.state = data
        if data is None:
            self.setup_state(filename)

    def setup_state(self, filename):
        try:
            with open(filename, "r") as file:
                # Read file
                data = file.read()
                # Delete newline
                data = data.replace("\r\n", "")
                data = data.replace("\n", "")
                # Store state
                self.state = list(data)
                # State checking
                if len(self.state) != 9:
                    raise ValueError("Wrong initial state, 3x3 matrix required")
                if self.state[4] != '-':
                    raise ValueError("Wrong initial state, middle element must be -")
                for i in range(len(self.state)):
                    if i != 4 and self.state[i] != '0' and self.state[i] != '1':
                        row = i // 3
                        column = i % 3
                        raise ValueError("Wrong initial state, illegal character at [{}, {}]".format(row, column))

        except Exception as e:
            traceback.print_exc()
            state = [
                '0', '0', '0',
                '0', '-', '0',
                '0', '0', '0'
            ]

    def is_oned(self):
        return np.array_equal(self.state, [
            '1', '1', '1',
            '1', '-', '1',
            '1', '1', '1'
        ])

    def is_zerod(self):
        return np.array_equal(self.state, [
            '0', '0', '0',
            '0', '-', '0',
            '0', '0', '0'
        ])

    def is_win(self, condition=None):
        # Win condition does not matter '0' or '1'
        if condition is None:
            return self.is_zerod() or self.is_oned()
        # Win condition is False == '0'
        if not condition:
            return self.is_zerod()
        # Win condition is True == '1'
        if condition:
            return self.is_oned()

    # Print state
    def print(self):
        # Start
        print("[")
        # Row 1
        print("\t" + str(self.state[0]) + ",", end="")
        print("\t" + str(self.state[1]) + ",", end="")
        print("\t" + str(self.state[2]))
        # Row 2
        print("\t" + str(self.state[3]) + ",", end="")
        print("\t" + str(self.state[4]) + ",", end="")
        print("\t" + str(self.state[5]))
        # Row 3
        print("\t" + str(self.state[6]) + ",", end="")
        print("\t" + str(self.state[7]) + ",", end="")
        print("\t" + str(self.state[8]))
        # End
        print("]")


class Node:

    def __init__(self, value, parent=None, move=None):
        self.parent = parent
        self.value = value
        self.children = list()
        # How node was reached from parent
        self.move = move

    def add_children(self, children, move=None):
        child = Node(children, self, move)
        self.children.append(child)
        return child


class Solver:

    def __init__(self, state):
        # Initial state
        self.initial_state = state
        # Initial tree node
        self.root = Node(state, None)
        # Already existing states to prevent cycles
        self.states = list()
        # List of solutions - Nodes
        self.solutions = list()
        # Solve for initial state
        self.solve()

    def existing_state(self, state):
        arr = state.state
        for s in self.states:
            if np.array_equal(arr, s.state):
                return True
        return False

    def solve(self):
        if self.root is None or self.root.value is None:
            raise ValueError("Wrong initial state")

        current_state = self.root.value
        current_node = self.root

        # Solve puzzle by recursive method
        self.solve_rec(current_state, current_node)

        # Print solution count
        print("Solutions found: {}".format(len(self.solutions)))

        # Solution console
        self.console()

    def console(self):
        if len(self.solutions) < 1:
            print("There are no solutions!")
            return

        if len(self.solutions) == 1:
            self.print_solution(0)
            return

        # There are multiple solutions
        print("There are {} solutions.".format(len(self.solutions)))

        while True:
            print("Choose solution 0-{}: ".format(len(self.solutions) - 1))
            solution = input()
            try:
                # Try to retype as int
                solution = int(solution)
                # Check range
                if solution >= len(self.solutions) or solution < 0:
                    raise Exception("Solution out of bounds")
                # print solution by number and end
                self.print_solution(solution)
                break

            except:
                print("Please select solution by number between 0 and {}".format(len(self.solutions) - 1))

    def translate_action(self, action):
        if action == "action0":
            return "TOP LEFT"
        if action == "action1":
            return "TOP CENTER"
        if action == "action2":
            return "TOP RIGHT"
        if action == "action3":
            return "CENTER LEFT"
        # No action for center
        if action == "action5":
            return "CENTER RIGHT"
        if action == "action6":
            return "BOTTOM LEFT"
        if action == "action7":
            return "BOTTOM CENTER"
        if action == "action8":
            return "BOTTOM RIGHT"

        return "UNKNOWN ACTION"

    def print_solution(self, index):
        actions = list()

        # Start at end
        current = self.solutions[index]

        while True:
            if current.parent is None:
                break

            actions.append(self.translate_action(current.move))

            # Move to parent until root element
            current = current.parent

        # reverse list
        actions = reversed(actions)

        # print list
        for a in actions:
            print(a)



    def solve_rec(self, state, node):

        new_states = self.actions(state)

        for key in new_states:
            new_state = new_states[key]

            # Ignore already explored states
            if self.existing_state(new_state):
                continue

            # Add state to explored
            self.states.append(new_state)

            # Get children node
            new_node = node.add_children(new_state, key)

            # Add node as solution if its valid
            if new_state.is_win():
                self.solutions.append(new_node)
                continue

            # Recursively visit other states
            self.solve_rec(new_state, new_node)

    # Top left activation
    def action0(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[0] = '0' if new_state[0] == '1' else '1'
        # Invert others
        new_state[1] = '0' if new_state[1] == '1' else '1'
        new_state[3] = '0' if new_state[3] == '1' else '1'
        return State(data=new_state)

    # Top center activation
    def action1(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[1] = '0' if new_state[1] == '1' else '1'
        # Invert others
        new_state[0] = '0' if new_state[0] == '1' else '1'
        new_state[2] = '0' if new_state[2] == '1' else '1'
        return State(data=new_state)

    # Top right activation
    def action2(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[2] = '0' if new_state[2] == '1' else '1'
        # Invert others
        new_state[1] = '0' if new_state[1] == '1' else '1'
        new_state[5] = '0' if new_state[5] == '1' else '1'
        return State(data=new_state)

    # Center left activation
    def action3(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[3] = '0' if new_state[3] == '1' else '1'
        # Invert others
        new_state[0] = '0' if new_state[0] == '1' else '1'
        new_state[6] = '0' if new_state[6] == '1' else '1'
        return State(data=new_state)

    # Center right
    def action5(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[5] = '0' if new_state[5] == '1' else '1'
        # Invert others
        new_state[2] = '0' if new_state[2] == '1' else '1'
        new_state[8] = '0' if new_state[8] == '1' else '1'
        return State(data=new_state)

    # Bottom left
    def action6(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[6] = '0' if new_state[6] == '1' else '1'
        # Invert others
        new_state[3] = '0' if new_state[3] == '1' else '1'
        new_state[7] = '0' if new_state[7] == '1' else '1'
        return State(data=new_state)

    # Bottom center
    def action7(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[7] = '0' if new_state[7] == '1' else '1'
        # Invert others
        new_state[6] = '0' if new_state[6] == '1' else '1'
        new_state[8] = '0' if new_state[8] == '1' else '1'
        return State(data=new_state)

    # Bottom right
    def action8(self, state):
        new_state = state.state.copy()
        # Invert self
        new_state[8] = '0' if new_state[8] == '1' else '1'
        # Invert others
        new_state[7] = '0' if new_state[7] == '1' else '1'
        new_state[5] = '0' if new_state[5] == '1' else '1'
        return State(data=new_state)

    # All actions
    def actions(self, state):
        states = dict()
        states["action0"] = self.action0(state)
        states["action1"] = self.action1(state)
        states["action2"] = self.action2(state)
        states["action3"] = self.action3(state)
        # Center has no action
        states["action5"] = self.action5(state)
        states["action6"] = self.action6(state)
        states["action7"] = self.action7(state)
        states["action8"] = self.action8(state)
        # Return all actions
        return states


if __name__ == '__main__':
    args = arg_parse()
    state = State(filename=args.file)
    solver = Solver(state)
