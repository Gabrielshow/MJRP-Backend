import math

# Define parameters
item_num = 6
buyer_num = 2



# Given parameters
# S = 1000	# Major setup cost
# s = [[350, 300, 320, 400, 400, 300], [250, 200, 300, 420, 450, 400]]  # Minor setup cost when item i is included in a group replenishment in buyer j
# v = [50, 50, 50, 50, 50, 50]  # Unit variable cost of item i
# r = [5, 5, 5, 5, 5, 5]  # Inventory carrying charge per unit time
# demand = [[10000, 5000, 3000, 1000, 600, 200], [8000, 1000, 12000, 6000, 4500, 100]]	#demand per unit time
# k_ij = [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]] 

# Function to compute cycle time
def cycle_time(k, t):
    T = k * t
    return T

# Function to compute order quantity
def order_quantity(demand, T):
    Q = []
    for i in range(buyer_num):
        buyer_demand = []
        for j in range(item_num):
            buyer_demand.append(T * demand[i][j])
        Q.append(buyer_demand)
    return Q

# Function to compute holding cost
def holding_cost(Q, v, r):
    total_holding_cost = 0
    for i in range(buyer_num):
        for j in range(item_num):
            total_holding_cost += (Q[i][j] * v[j] * r[j]) / 2
    return total_holding_cost

# Function to compute setup costs
def set_up_costs(k, T):
    cons = S / T
    set_up_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            set_up_cost = s[i][j] / (k[i][j] * T)
            set_up_array.append(set_up_cost)
    total_set_up_cost = cons + sum(set_up_array)
    return total_set_up_cost

# Function to compute total annual cost
def total_annual_cost(Q, T):
    total_holding_cost = holding_cost(Q, v, r)
    total_setup_cost = set_up_costs(Q, T)
    return total_holding_cost + total_setup_cost


# Goyal Algorithm
def goyal_algorithm(demand, k_ij):
    # Step 1: Initialize parameters
    t_max = find_cycle_time_max()
    t_min = find_cycle_time_min()

    # Step 2: Initialize variables
    T_p = t_min  # Start with the minimum cycle time
    q = 0  # Initialize iteration counter
    converged = False

    # Step 3: Iterate until convergence
    while not converged:
        # Step 4: Compute k_ijq
        k_ijq = compute_k_ijq(T_p, q, demand)

        # Step 5: Find k_ijq for each i and j
        # This step is already included in the computation of k_ijq

        # Step 6: Compute new cycle time T_p
        T_p = compute_new_cycle_time(k_ijq)

        # Step 7: Check for convergence
        if q == 1 or not_condition_met(k_ijq):
            q += 1
        else:
            converged = True

    return T_p, k_ijq

# Function to compute k_ijq
def compute_k_ijq(T_p, q, demand):
    k_ijq = []
    for i in range(buyer_num):
        for j in range(item_num):
            k_ijq.append(2 * s[i][j] * T_p**2 / math.sqrt(r[j] * demand[i][j] * v[i]))
    return k_ijq

# Function to compute new cycle time T_p
def compute_new_cycle_time(k_ijq):
    numerator = 2 * S
    denominator = sum(k_ijq)
    T_p = math.sqrt(numerator / denominator)
    return T_p

# Function to check condition for Step 7
def not_condition_met(k_ijq):
    # Check if kp_ijq - kp_ijq-1 = 1 for any i and j
    # If condition is met, return True; otherwise, return False
    # Implementation depends on specific condition in your problem
    return False

# Helper functions and functions for finding t_max and t_min (to be implemented)
def func1(item_num, buyer_num, s, S):
    set_up_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            set_up_array.append(s[i][j])
    return S + sum(set_up_array)
    
def func2(item_num, buyer_num, d, v, r):
    demand_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            demand_array.append(d[i][j]*v[j])
    return sum([r[j] * demand_array[j] for j in range(len(r))])

# functions to find tmax
def find_cycle_time_max():
    var_1 = func1(item_num, buyer_num, s, S)
    var_2 = func2(item_num, buyer_num, demand, v, r)
    T_max = math.sqrt((2 * var_1)/var_2)
    return round(T_max)

#functions to find Tmin
# helper functions for tmin
def t1_helper_function(s, r, d, v, buyer_num, item_num):
    t1_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            t_variable = math.sqrt((2 * s) / (r * d * v))
            t1_array.append(t_variable)
            return min(t1_array)

# code for finding the minimum cycle time
def find_t1(s, r, demand, v):
    t1_min = float('inf')
    
    # iteration over all elements of the demand matrix
    for i in range(buyer_num):
        for j in range(item_num):
            expr = math.sqrt((2 * s[i][j]) / (r[j] * demand[i][j] * v[i]))
            t1_min = min(t1_min, expr)
    
    return t1_min
            
def func_min1(s, k, buyer_num, item_num, S, t1):
    array1 = []
    for i in range(buyer_num):
        for j in range(item_num):
            set_up_cost = s[i][j]/(k[i][j] * t1)
            array1.append(set_up_cost)
    return S + sum(array1)

def func_min2(d, v, k, r, buyer_num, item_num, t1):
    array2 = []
    for i in range(buyer_num):
        for j in range(item_num):
            demand_cost = d[i][j] * v[i] / k[i][j] * t1
            array2.append(demand_cost)
    return sum([r[i] * array2[i] for i in range(len(r))])

def find_cycle_time_min():
    t1 = find_t1(s, r, demand, v)
    var_1 = func_min1(s, k_ij, buyer_num, item_num, S, t1)
    var_2 = func_min2(demand, v, k_ij, r, buyer_num, item_num, t1)
    Tmin = math.sqrt((2 * var_1)/ var_2)
    return round(Tmin)

def calculate_cost(parameters):
    # Initialize variables to store extracted parameters
    demand = None
    s = None
    k_ij = None
    S = None
    # Add other parameters as needed

    # Iterate over the list of parameters
    for param_name, param_value in parameters.items():  # Use items() to iterate over key-value pairs
        if param_name == 'Demand':
            demand = param_value
        elif param_name == 'Holding Cost':
            s = param_value
        elif param_name == 'Time Multipliers':
            k_ij = param_value
        elif param_name == 'Major Setup Cost':
            S = param_value
        # Add other parameters as needed

    # Check if all required parameters are extracted
    if demand is None or s is None or k_ij is None or S is None:
        return {"error": "Required parameters not provided"}

    # Run Goyal algorithm with the provided parameters
    T_p, k_ijq = goyal_algorithm(demand, k_ij)

    # Use the optimal T_p and k_ijq to compute the optimal order quantity Q
    Q = order_quantity(demand, T_p)

    # Compute total relevant cost
    C = total_annual_cost(Q, T_p)

    return {"success": "Parameters extracted successfully"}

# Main function
def main():
    # Run Goyal algorithm
    # mjrp.py

    T_p, k_ijq = goyal_algorithm(demand, k_ij)

    # Use the optimal T_p and k_ijq to compute the optimal order quantity Q
    Q = order_quantity(demand, T_p)

    # Compute total relevant cost
    C = total_annual_cost(Q, T_p)

    print("Optimal cycle time T_p:", T_p)
    print("Optimal order quantity Q:", Q)
    print("Total relevant cost C:", C)

# Execute main function
if __name__ == "__main__":
    main()
