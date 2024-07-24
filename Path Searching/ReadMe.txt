# Path Searching using DFS and BFS algorithms for non informed searches and A* Search and Greedy Best-First Search for informed searches.

Problem: In a given map, where the cities are the nodes and the edges are the routes between them, find the shortest path from a city to another. This map is defined in the csv files as given:
        - map.csv - contains the names of the cities and thei IDs
        - graph.csv - contains the routes availbe between each city and the distances of those routes
        - heuristic - contains the straight line distances between each city and 'Bucharest', as the goal city for the informed searches in this problem will always be 'Bucharest'

Depth-Frist Search

  Versatile algorithm useful for exploring all possible paths in a graph, particularly when the solution is expected to be deep in the graph rather than close to the starting point.
  Uses a stack data structure to keep track of the nodes to be explored. This stack can be implemented explicitly using a stack data (Last In, First Out) structure or implicitly using recursion. For this problem I used a stack data structure to show the difference between stacks and queues
  Starts at a given node and explores as far as possible along each branch before backtracking. This means it goes deep into the graph first before moving to the next branch.
  Steps:
        1.Initialize - Start at the initial node, mark it as visited, and push it onto the stack.
        2.Loop - While the stack is not empty:
            Pop a node from the stack.
            For each unvisited neighbor of this node, mark it as visited and push it onto the stack.
        3.Repeat - Continue this process until all nodes are visited or a specific condition (such as finding a target node) is met.

Breadth-First Search

  Similar to DFS, but it explores all the nodes at the present depth level before moving on to the nodes at the next depth level. This means it explores all nodes one level away, then all nodes two levels away, and so on.
  Uses a queue data structure to keep track of the nodes to be explored. Nodes are added to the queue in the order they are discovered and are processed in a first-in, first-out (FIFO) manner.
  Steps:
        1.Initialize - Start at the initial node, mark it as visited, and enqueue it.
        2.Loop - While the queue is not empty:
            Dequeue a node from the queue.
            For each unvisited neighbor of this node, mark it as visited and enqueue it.
        3.Repeat - Continue this process until all nodes are visited or a specific condition (such as finding a target node) is met.

Greedy Best-First Search

  Greedy Best-First Search is a fast and straightforward algorithm that uses heuristics to guide its search. While it can quickly find a path in many cases, it does not guarantee the shortest path or even a path at all if one exists. It's best used when speed is more critical than optimality and completeness, and when a good heuristic is available to guide the search effectively.
  It always expands the node that appears to be closest to the goal, according to the heuristic.
  Key Concepts:
      - Heuristic Function (h(n)):
          This function estimates the cost from the current node to the goal.
          A good heuristic is crucial for the performance of GBFS.
      - Priority Queue:
          Nodes are stored in a priority queue (often implemented as a min-heap).
          Nodes are prioritized based on their heuristic value (h(n)).
  Steps:
      1.Initialization
        Start with the initial node and calculate its heuristic value.
        Add the initial node to the priority queue.
      2.Main Loop
        While the priority queue is not empty:
            Remove the node with the lowest heuristic value from the queue.
            If this node is the goal, reconstruct and return the path.
            Otherwise, for each neighbor of this node:
                Calculate the heuristic value for the neighbor.
                If the neighbor has not been visited or has a better heuristic value than previously recorded, add it to the priority queue.
      3.Termination
        If the goal is reached, return the path.
        If the priority queue is empty and the goal has not been reached, return failure (no path exists).

A* Search

  A* combines the strengths of both Dijkstra's algorithm and Greedy Best-First-Search by considering both the cost to reach a node and an estimate of the cost to reach the goal from that node.
  Key concepts:
      - Priority Queue: A* uses a priority queue (often implemented with a min-heap) to keep track of nodes to be explored, prioritizing nodes based on their total estimated cost.
      - Cost Functions:
          g(n): The exact cost from the starting node to node n.
          h(n): A heuristic function that estimates the cost from node n to the goal node.
          f(n) = g(n) + h(n): The estimated total cost of the cheapest solution through node n.
      - Heuristic: The heuristic function h(n) is crucial to the efficiency of A*. It must be admissible, meaning it never overestimates the true cost to reach the goal, and consistent, meaning the estimated cost is always less than or equal to the estimated cost from any neighboring node plus the step cost.
  Steps:
      1.Initialize
        Start with the initial node, calculate its f(n) value, and add it to the priority queue.
      2.Loop
        While the priority queue is not empty:
            Remove the node with the lowest f(n) value from the queue.
            If this node is the goal, reconstruct and return the path.
            For each neighbor of this node:
                Calculate the g(n) value for the neighbor.
                Calculate the f(n) value for the neighbor.
                If the neighbor has not been visited or has a lower f(n) value than previously recorded, add it to the priority queue.
      3.Repeat
        Continue this process until the goal is reached or the priority queue is empty (indicating no path exists).
