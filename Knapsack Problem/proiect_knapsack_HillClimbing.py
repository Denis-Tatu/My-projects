import random
import pandas as pd

# Reading item data and knapsack properties from CSV files
items_data = pd.read_csv("items.csv")
items = {}

# Iterating through each row of the items data and storing value and weight of each item
for i,row in items_data.iterrows():
    item = {'value' : row['value'], 'weight' : row['weight']}
    items[f'item{i + 1}'] = item

# Reading the knapsack data from CSV, which contains capacity and optimal selection details
knapsack_data = pd.read_csv("knapsack.csv")
row = knapsack_data.loc[0]

# Extracting the knapsack's capacity and optimal solution details
capacity = int(row['capacity'])
op_selection_binary = row['optimal_selection'].strip("'") # Optimal item selection in binary form
op_weight = int(row['optimal_weight'])
op_value = int(row['optimal_value'])

# Converting the binary string to a dictionary indicating selected items in the optimal solution
op_selection = {f'item{i + 1}': bool(int(bit)) for i, bit in enumerate(op_selection_binary)}

# Function to evaluate the total value and weight of a given selection
def evaluate_knapsack(selection):
    total_value = 0
    total_weight = 0
    for item, selected in selection.items():
        if selected: # If the item is selected, add its value and weight
            total_value += items[item]['value']
            total_weight += items[item]['weight']
    if total_weight > capacity: # If the total weight exceeds capacity, return 0 value, else return the actual total
        return 0, total_weight
    else:
        return total_value, total_weight
    
# Function to return the binary representation of a selection (1 for selected, 0 for not selected)
def binary_representation(selection):
    return ''.join(['1' if selected else '0' for selected in selection.values()])

# Hill Climbing algorithm to find the best selection
def hill_climbing():
    # Generate a random selection until the weight is within the knapsack's capacity
    current_weight = capacity + 1
    while current_weight > capacity:
        current_selection = {item: random.choice([True, False]) for item in items}
        current_value, current_weight = evaluate_knapsack(current_selection)

    # Print initial selection and its value, weight, and temperature
    print("Initial Random Selection:", current_selection)
    print("Binary Representation:", binary_representation(current_selection))
    print("Initial Random Selection Value:", current_value)
    print("Initial Random Selection Weight:", current_weight)
    print()
    
    i = 1

    while True:
        neighbors = [] # List to store all neighboring solutions
        for item in items: # Generate all neighbors by flipping one item's selection at a time
            neighbor_selection = current_selection.copy()
            neighbor_selection[item] = not neighbor_selection[item]
            neighbors.append((neighbor_selection, *evaluate_knapsack(neighbor_selection)))

        # Find the best neighbor (the one with the highest value)
        best_neighbor = max(neighbors, key=lambda x: x[1])
        if best_neighbor[1] > current_value: # If the best neighbor is better than the current selection, move to the neighbor
            current_selection = best_neighbor[0]
            current_value = best_neighbor[1]
            current_weight = best_neighbor[2]

            # Print the intermediate selection details
            print(f"Intermediate Selection {i}:", current_selection)
            print("Binary Representation:", binary_representation(current_selection))
            print("Intermediate Selection Value:", current_value)
            print("Intermediate Selection Weight:", current_weight)
            print()
            i = i + 1
        else:
            break # Stop if no better neighbor is found

    # If final solution exceeds capacity, set the value to 0
    if current_weight > capacity:
        current_value = 0
    return current_selection, current_value, current_weight, i

# Execute the hill climbing algorithm
best_selection, best_value, best_weight, nr = hill_climbing()

# Print final results of the algorithm
print("Best Selection Found:", best_selection)
print("Binary Representation:", binary_representation(best_selection))
print("Final Value:", best_value)
print("Final Weight:", best_weight)
print("Total Selections:", nr)
print()

# Compare with the optimal solution
print("Optimal Solutin:", op_selection)
print("Binary Representation:", op_selection_binary)
print("Optimal Value:", op_value)
print("Optimal Weight:", op_weight)
print()

# Calculate and print the errors and accuracy
print("Value error:", op_value - best_value)
print("Weight error:", op_weight - best_weight)
print("Value accuracy: {:.2f}%".format(best_value * 100 / op_value))
print("Weight accuracy: {:.2f}%".format(best_weight * 100 / op_weight))
