import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import re

# Getting data from csv files
graph = pd.read_csv('graph.csv')
map = pd.read_csv('map.csv')

# Creating the graph's matrix based on the adjacency list from the csv file
num_rows = map.shape[0]
matrix = np.zeros([num_rows, num_rows])

for i, row in graph.iterrows():
    x = row['ID_C1']
    y = row['ID_C2']
    matrix[x - 1, y - 1] = matrix[y - 1, x - 1] = 1

nodes = 0  # the total number of nodes generated
number_solutions = 0  # the number of solutions to be found

# Getting the 'states' list based on the csv file, in this case the list of cities on the map
states = list(range(num_rows))

for i, row in map.iterrows():
    x = row['ID']
    y = row['City_name']
    states[x - 1] = y

class Node:
    def __init__(self, index: int, state: str, parent, transition: str, level: int, value: int):
        """The parent is a reference to the Node that is the parent of the current node, in the search tree"""
        global nodes
        nodes = nodes + 1
        self.index = index
        self.state = state
        self.parent = parent
        self.transition = transition
        self.level = level
        self.value = value

    def get_path(self) -> str:
        """Build the string representation of the path from the root to the current Node (parsing it
        backwards)."""
        current = self
        s = self.state
        current = current.parent
        while current:
            s = str(current.state) + "->" + s
            current = current.parent
        return s

    def __str__(self):
        """The string representation of the current node. The node represents an actual path in the search tree,
         hence the path gets printed also. """
        s = ""
        s = s + str(self.state)
        s = s + "(" + self.get_path() + ")"
        return s

    def closed_cycle(self, s: str) -> bool:
        """Check if the state s (as a string) is found on the path from the root to the current node
        In case it is, it means that s would close a cycle on this path."""
        current = self
        while current:
            if current.state == s:
                return True
            current = current.parent
        return False


class Graph:
    """The class Graph stores the information on the problem."""

    def __init__(self, matrix, states, start_index, goal_state):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != matrix[j][i]:
                    messagebox.showerror("Not a square matrix !")
        self.matrix = matrix
        self.states = states
        for i, row in map.iterrows():
            if row['City_name'] == start_index:
                self.start_index = row['ID'] - 1
                break
        self.goal_state = goal_state

    def generate_successors(self, n: Node) -> list[Node]:
        """The successor function depends on the data related to the problem.
        All the nodes connected to the current state are encapsulated and made as successor"""
        l = len(self.matrix)
        succ = []
        for i in range(l):
            if self.matrix[n.index][i] != 0:
                s = Node(i, states[i], n, states[i], n.level + 1,0)  # transition is the state of this successor
                succ.append(s)
        return succ

    def breadth_first_search(self, nsol: int):
        """BFS starts with the root. It stores two lists:
                the frontier - the nodes that were not expanded yet
                the visited - nodes that were explored (expanded) already"""
        message = ""

        global nodes, number_solutions
        nodes = 0
        number_solutions = 0

        start_time = time.time()

        start = Node(self.start_index, states[self.start_index], None, "", 0, 0)
        goal = self.goal_state

        # The frontier is initialized with the Node that represents the initial state.
        # In BFS, the frontier is organized as a queue which gives the breadth like search for the graph.
        # At first, the visited list is empty.
        frontier = [start]
        visited = []

        # while there exist nodes that were not visited yet (on the frontier)
        # and the goal state was not yet reached
        while frontier:
            # print the current frontier
            message += "Frontier: [\n"
            for x in frontier:
                message += str(x) + "\n"
            message += "]\n\n"

            current = frontier[0]
            frontier.remove(current)
            if current.state == goal:
                number_solutions = number_solutions + 1
                message += "BFS SUCCESS\n"
                message += current.get_path() + "\n"
                message += "Depth: " + str(current.level) + "\n"
                message += "Nodes: " + str(nodes) + "\n"
                message += "Execution time: " + str(time.time() - start_time) + "\n\n"
                if number_solutions >= nsol:
                    return message, current.get_path()

            visited.append(current)
            successors = self.generate_successors(current)

            for s in successors:
                if s in frontier or s in visited:
                    continue
                if current.closed_cycle(s.state):
                    continue
                frontier.append(s)

        message += "BFS FAILURE: There is no path\n"
        message += "Nodes created by BFS: " + str(nodes)

        return message, current.get_path()

    def depth_first_search(self, nsol: int):
        """Similar to BFS, the difference being the usage of STACK, instead of QUEUE, giving the depth like search"""

        message = ""

        global nodes, number_solutions
        number_solutions = 0
        nodes = 0
        start = Node(self.start_index, states[self.start_index], None, "", 0, 0)
        goal = self.goal_state

        frontier = [start]
        visited = []

        start_time = time.time()

        while frontier:
            message += "Frontier: [\n"
            for x in frontier:
                message += str(x) + "\n"
            message += "]\n\n"

            # the frontier is organized as a STACK. The Last element In, is the First to be popped out.
            current = frontier[-1]
            frontier.remove(current)
            if current.state == goal:
                number_solutions = number_solutions + 1
                message += "DFS SUCCESS\n"
                message += current.get_path() + "\n"
                message += "Depth: " + str(current.level) + "\n"
                message += "Nodes: " + str(nodes) + "\n"
                message += "Execution time: " + str(time.time() - start_time) + "\n\n"
                if number_solutions >= nsol:
                    return message, current.get_path()

            visited.append(current)
            successors = self.generate_successors(current)

            for s in successors:
                if s in frontier or s in visited:
                    continue
                if current.closed_cycle(s.state):
                    continue
                frontier.append(s)
        message += "DFS FAILURE: There is no path\n"
        message += "Nodes created by BFS: " + str(nodes)

        return message, current.get_path()

# Define tkinter GUI
class GraphSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("Route search with DFS and BFS")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 2350) // 2
        y = (screen_height - 670) // 2
        self.root.geometry(f"{2350}x{670}+{x}+{y}")
        self.root.configure(bg='#462763')

        self.mainFrame = tk.Frame(self.root, bg='lightblue')
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.columnconfigure(2, weight=1)

        self.leftFrame = tk.Frame(self.mainFrame, bg='lightblue')
        self.leftFrame.columnconfigure(0, weight=1)
        self.leftFrame.columnconfigure(1, weight=1)

        # Add widgets like radio buttons, dropdowns, etc.
        self.algorithm_var = tk.IntVar()
        self.algorithm_var.set(1)

        self.dfs_check = tk.Radiobutton(self.leftFrame, text="Depth First Search", variable=self.algorithm_var, value=1, font=('Arial',14), bg='lightblue')
        self.dfs_check.grid(row=0, column=0, sticky=tk.W+tk.N, padx=20, pady=30)

        self.bfs_check = tk.Radiobutton(self.leftFrame, text="Breadth First Search", variable=self.algorithm_var, value=2, font=('Arial',14), bg='lightblue')
        self.bfs_check.grid(row=0, column=1, sticky=tk.W+tk.N, pady=30)

        self.start_state_label = tk.Label(self.leftFrame, text="Select the state from where to start searching:", font=('Arial', 14), bg='lightblue')
        self.start_state_label.grid(row=1, column=0, sticky=tk.W + tk.N, pady=25)

        self.start_state_var = tk.StringVar()
        self.start_state_var.set(sorted(states)[0])

        self.start_dm = tk.OptionMenu(self.leftFrame, self.start_state_var, *sorted(states))
        self.start_dm.config(font=('Arial', 14), width=10, bg='#6975CD', fg='white')
        self.start_dm.grid(row=1, column=1, sticky=tk.W + tk.E, padx=35, pady=25)

        self.end_state_label = tk.Label(self.leftFrame, text="Select the state where the search ends:", font=('Arial', 14), bg='lightblue')
        self.end_state_label.grid(row=2, column=0, sticky=tk.W + tk.N, pady=25)

        self.end_state_var = tk.StringVar()
        self.end_state_var.set(sorted(states)[0])

        self.end_dm = tk.OptionMenu(self.leftFrame, self.end_state_var, *sorted(states))
        self.end_dm.config(font=('Arial', 14), width=10, bg='#6975CD', fg='white')
        self.end_dm.grid(row=2, column=1, sticky=tk.W + tk.E, padx=35, pady=25)

        self.solutions_label = tk.Label(self.leftFrame, text="Select the number of solutions to be given:", font=('Arial', 14), bg='lightblue')
        self.solutions_label.grid(row=3, column=0, sticky=tk.W + tk.N, pady=25)

        self.solutions_var = tk.IntVar()
        self.solutions_var.set(1)
        self.nr = [1, 2, 3, 4, 5]

        self.sol_dm = tk.OptionMenu(self.leftFrame, self.solutions_var, *sorted(self.nr))
        self.sol_dm.config(font=('Arial', 14), bg='#6975CD', fg='white')
        self.sol_dm.grid(row=3, column=1, sticky=tk.W + tk.E, padx=35, pady=25)

        self.start_button = tk.Button(self.leftFrame, text="Start Search", command=self.start_search, font=('Arial',14), bg='#6975CD', fg='white')
        self.start_button.grid(row=4, column=0, columnspan=2, pady=40)

        self.leftFrame.grid(row=0, column=0, sticky=tk.W+tk.N)

        self.centerFrame = tk.Frame(self.mainFrame)
        self.centerFrame.columnconfigure(0, weight=1)

        self.view = tk.Canvas(self.centerFrame)
        self.view.grid(row=1, column=0)

        self.edges = []
        self.labels = {}
        # build the list of edges as pairs (i,j)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != 0:
                    self. edges.append((i, j))
        # build the graph
        self.graph_draw = nx.Graph(self.edges)
        # build the list of labels for the nodes in the graph using the states
        for i in self.graph_draw.nodes:
            self.labels.update({i: states[i]})

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.pos = nx.kamada_kawai_layout(self.graph_draw)
        nx.draw(self.graph_draw, self.pos, ax=self.ax, with_labels=False)
        nx.draw_networkx_labels(self.graph_draw, self.pos, labels=self.labels, ax=self.ax)

        self.view_agg = FigureCanvasTkAgg(self.fig, master=self.view)
        self.view_agg.draw()
        self.view_agg.get_tk_widget().pack()

        self.centerFrame.grid(row=0, column=1)

        self.rightFrame = tk.Frame(self.mainFrame)
        self.rightFrame.columnconfigure(0, weight=1)

        self.text = tk.Text(self.rightFrame, font=('Arial',14), height=27)
        self.text.configure(state='disabled')
        self.text.grid(row=0, column=0, sticky=tk.W+tk.N)

        self.rightFrame.grid(row=0, column=2, sticky=tk.W+tk.N, padx=10)

        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
            plt.close()  # Close matplotlib figure
            self.root.destroy()  # Close tkinter window

    def highlight_path(self, state_indices):
        # Clear previous highlights
        for node in self.graph_draw.nodes:
            self.graph_draw.nodes[node]['color'] = 'blue'  # Reset node colors
        for edge in self.graph_draw.edges:
            self.graph_draw.edges[edge]['color'] = 'black'  # Reset edge colors

        # Color nodes and edges in the path using state indices
        for i in range(len(state_indices) - 1):
            u_idx = state_indices[i]
            v_idx = state_indices[i + 1]

            self.graph_draw.nodes[u_idx]['color'] = 'red'  # Highlight nodes
            self.graph_draw.edges[u_idx, v_idx]['color'] = 'red'  # Highlight edges

        # Color the start and end nodes differently
        if state_indices:
            self.graph_draw.nodes[state_indices[0]]['color'] = 'green'  # Start node
            self.graph_draw.nodes[state_indices[-1]]['color'] = 'orange'  # End node

        # Update the matplotlib figure with the new colors
        self.ax.clear()
        nx.draw(self.graph_draw, self.pos, ax=self.ax, with_labels=False,
                node_color=[self.graph_draw.nodes[node]['color'] for node in self.graph_draw.nodes],
                edge_color=[self.graph_draw.edges[edge]['color'] for edge in self.graph_draw.edges])
        nx.draw_networkx_labels(self.graph_draw, self.pos, labels=self.labels, ax=self.ax)

        self.view_agg.draw()

    def start_search(self):
        start_state = self.start_state_var.get()
        end_state = self.end_state_var.get()
        num_solutions = self.solutions_var.get()
        algorithm = self.algorithm_var.get()

        p = Graph(matrix, states, start_state, end_state)

        if algorithm == 1:
            message, path = p.depth_first_search(num_solutions)
        elif algorithm == 2:
            message, path = p.breadth_first_search(num_solutions)

        self.text.configure(state='normal')
        self.text.insert(tk.END, message)
        self.text.see(tk.END)
        self.text.configure(state='disabled')

        # Extract state names from path string
        pattern = r'([^\->]+)'
        state_names = re.findall(pattern, path)

        # Convert state names to their corresponding indices in the states list
        state_indices = []
        for state in state_names:
            idx = states.index(state)
            state_indices.append(idx)

        # Highlight the path on the matplotlib figure
        self.highlight_path(state_indices)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = GraphSearch(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
