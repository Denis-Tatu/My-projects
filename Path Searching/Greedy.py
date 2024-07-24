from queue import PriorityQueue
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
distance_matrix = np.zeros([num_rows, num_rows]) # also, the distance matrix giving us the weights of the edges
for i, row in graph.iterrows():
    x = row['ID_C1']
    y = row['ID_C2']
    matrix[x - 1, y - 1] = matrix[y - 1, x - 1] = 1
    distance_matrix[x - 1, y - 1] = distance_matrix[y - 1, x - 1] = row['Distance']

nodes = 0  # the total number of nodes generated
number_solutions = 0  # the number of solutions to be found

# Getting the 'states' list based on the csv file, in this case the list of cities on the map
states = list(range(num_rows))

for i, row in map.iterrows():
    x = row['ID']
    y = row['City_name']
    states[x - 1] = y


class Node:
    def __init__(self, index: int, state: str, parent, transition: str, level: int, value: int, cost: int):
        """The parent is a reference to the Node that is the parent of the current node, in the search tree
        The heuristic cost is represented by the straight line distances, in this case, between each state and Bucharest.
        Its purpose is to estimate the cost to the goal state, improving pathfinding efficiency"""
        global nodes
        nodes = nodes + 1
        self.index = index
        self.state = state
        self.parent = parent
        self.transition = transition
        self.level = level
        self.value = value
        self.cost = cost

    def __lt__(self, other):
        """Defining the behaviour of the less-than(<) operator for these instances of the class in order to be able to compare
        nodes and since this algorithm uses a priority queue, the comparison is based on the estimated distance remained till goal state"""
        return self.value < other.value

    def get_path(self) -> str:
        """Build the string representation of the path from the root to the current Node (parsing it backwards)."""
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
        s += f"State: {self.state}, Path: {self.get_path()}, Distance remained: {self.cost}\n"
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
    def __init__(self, matrix, distance_matrix, states, start_index, goal_state):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != matrix[j][i]:
                    messagebox.showerror("Not a square matrix")
        self.matrix = matrix
        self.distance_matrix = distance_matrix
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
                s = Node(i, states[i], n, states[i], n.level + 1, 0, self.heuristic(i))
                succ.append(s)
        return succ

    def greedy_best_first_search(self, nsol: int):
        """BFS based algorithm that uses a priority queue to explore nodes, prioritizing nodes with the least total
        distance remained till goal state, so it only uses the heuristic values. The efficiency of this algorithm resides
        in always choosing the node that is closest to the goal."""
        message = ""

        global nodes, number_solutions
        nodes = 0
        number_solutions = 0
        start = Node(self.start_index, states[self.start_index], None, "", 0, 0, self.heuristic(self.start_index))
        goal = self.goal_state
        frontier = PriorityQueue()
        frontier.put((0, start))

        visited = set()

        start_time = time.time()

        while not frontier.empty():
            message += "Frontier: [\n"
            for priority, node in frontier.queue:
                message += str(node)
            message += "]\n\n"

            _, current = frontier.get()

            if current.state == goal:
                number_solutions = number_solutions + 1
                message += "Greedy Best-First Search: SUCCESS\n"
                message += current.get_path() + "\n"
                message += "Distance remained: " + str(current.cost) + "\n"
                message += "Depth: " + str(current.level) + "\n"
                message += "Nodes: " + str(nodes) + "\n"
                message += "Execution time: " + str(time.time() - start_time) + "\n\n"
                if number_solutions >= nsol:
                    return message, current.get_path()

            visited.add(current.index)

            successors = self.generate_successors(current)

            for s in successors:
                if s.index in visited:
                    continue
                if current.closed_cycle(s.state):
                    continue
                priority = s.cost  # Using cost as priority in the priority queue
                frontier.put((priority, s))

        message += "Greedy Best-First Search: FAILURE - There is no path\n"
        message += "Nodes created by Greedy Best-First Search: " + str(nodes) + "\n"

        return message, current.get_path()

    def heuristic(self, current_index):
        # Getting the heuristic values from the csv file
        straight_line_distances = pd.read_csv('heuristic.csv')
        distance_row = straight_line_distances.loc[straight_line_distances['ID'] == current_index + 1]
        heuristic_value = distance_row['Distance_to_Bucharest'].values[0]
        return heuristic_value


# Define tkinter GUI
class GraphSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("Route search with Greedy Best-First")
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

        self.start_state_label = tk.Label(self.leftFrame, text="Select the state from where to start searching:", font=('Arial', 14), bg='lightblue')
        self.start_state_label.grid(row=0, column=0, sticky=tk.W + tk.N, pady=25)

        self.start_state_var = tk.StringVar()
        self.start_state_var.set(sorted(states)[0])

        self.start_dm = tk.OptionMenu(self.leftFrame, self.start_state_var, *sorted(states))
        self.start_dm.config(font=('Arial', 14), width=10, bg='#6975CD', fg='white')
        self.start_dm.grid(row=0, column=1, sticky=tk.W + tk.E, padx=35, pady=25)

        self.solutions_label = tk.Label(self.leftFrame, text="Select the number of solutions to be given:", font=('Arial', 14), bg='lightblue')
        self.solutions_label.grid(row=1, column=0, sticky=tk.W + tk.N, pady=25)

        self.solutions_var = tk.IntVar()
        self.solutions_var.set(1)
        self.nr = [1, 2, 3, 4, 5]

        self.sol_dm = tk.OptionMenu(self.leftFrame, self.solutions_var, *sorted(self.nr))
        self.sol_dm.config(font=('Arial', 14), bg='#6975CD', fg='white')
        self.sol_dm.grid(row=1, column=1, sticky=tk.W + tk.E, padx=35, pady=25)

        self.start_button = tk.Button(self.leftFrame, text="Start Search", command=self.start_search, font=('Arial',14), bg='#6975CD', fg='white')
        self.start_button.grid(row=2, column=0, columnspan=2, pady=40)

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

        # Add edge labels
        edge_labels = {(i, j): f'{distance_matrix[i, j]:.1f}' for i, j in self.graph_draw.edges()}
        nx.draw_networkx_edge_labels(self.graph_draw, self.pos, edge_labels=edge_labels, ax=self.ax,
                                     label_pos=0.5,  # Position at the center
                                     font_size=8,
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.1, pad=2),
                                     rotate=False)

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

        # Add edge labels
        edge_labels = {(i, j): f'{distance_matrix[i, j]:.1f}' for i, j in self.graph_draw.edges()}
        nx.draw_networkx_edge_labels(self.graph_draw, self.pos, edge_labels=edge_labels, ax=self.ax,
                                     label_pos=0.5,  # Position at the center
                                     font_size=10,
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.1, pad=2),
                                     rotate=False)

        self.view_agg.draw()

    def start_search(self):
        start_state = self.start_state_var.get()
        num_solutions = self.solutions_var.get()

        p = Graph(matrix, distance_matrix, states, start_state, 'Bucharest')

        message, path = p.greedy_best_first_search(num_solutions)

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
