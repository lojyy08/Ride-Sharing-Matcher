   # Read data from CSV file and categorize passengers and drivers based on their coordinates
import csv
# To calculate the Euclidean distance between passengers and drivers
import math
# To perform random matching of passengers and drivers
import random

# To visualize the locations of passengers and drivers (GUI)
import matplotlib.pyplot as plt


# Create a CSV file named 'data.csv' and write the header and random data for passengers and drivers
with open('data.csv', 'w', newline='') as file:
    # Create a CSV writer object to write data to the file
    writer = csv.writer(file)
    # Write the header row to the CSV file
    writer.writerow(["Type", "Name", "x", "y"])
    passenger_names = [
        "jana", "josephine", "lojy", "yassin", "mohamed", "sara", "ahmed", "lina", "omar", "nour",
        "khaled", "dina", "hassan", "farah", "yousef", "mariam", "tamer", "salma", "hany", "nadia"
    ]
    driver_names = [
        "mahmoud", "mariem", "yara", "hussein", "samar", "kareem", "dalia", "mohab", "laila", "mostafa"
    ]
    for i in range(1, 21):  # Loop to generate random coordinates for 20 passengers and write them to the CSV file
        writer.writerow(["Passenger", passenger_names[i-1],
                        random.randint(0, 100), random.randint(0, 100)])

    # Loop to generate random coordinates for 10 drivers and write them to the CSV file
    for i in range(1, 11):
        writer.writerow(["Driver", driver_names[i-1],
                        random.randint(0, 100), random.randint(0, 100)])

# Initialize empty lists to store passenger and driver coordinates
passengers = []
drivers = []

# 'try-except' used to handle potential file-related errors
try:
    # 'with' will automatically close the file after its block is executed (to avoid memory leaking)
    with open('data.csv', 'r') as file:
        # Create a CSV reader object to read the file
        reader = csv.reader(file)
        # To skip the header row (contains column names)
        next(reader)
        for row in reader:
            # Unpack the row into category, x, and y variables
            category, name, x, y = row
            x, y = int(x), int(y)
            # Normalize category string for consistent comparison
            category = category.strip().lower()
            if category == 'passenger':
                # Append passenger coordinates as a dictionary to the passengers list
                passengers.append({'name': name, 'x': x, 'y': y})
            else:
                # Append driver coordinates as a dictionary to the drivers list
                drivers.append({'name': name, 'x': x, 'y': y})
except FileNotFoundError:
    print("File not found. Please check the file path and try again.")
except Exception as e:                   # Catch any other exceptions that may occur and print the error message
    print(f"An error occurred: {e}")


# Calculate the Euclidean distance between a passenger and a driver
def distance(passenger, driver):
    return math.sqrt((passenger['x'] - driver['x']) ** 2 + (passenger['y'] - driver['y']) ** 2)


# Greedy algorithm to match passengers with drivers based on the shortest distance
def greedy_matching(passengers, drivers):
    used_passengers = set()   # To keep track of passengers that have already been matched
    used_drivers = set()      # To keep track of drivers that have already been matched
    matches = []              # To store the final matches between passengers and drivers
    total_dist = 0
    number_of_drivers = len(drivers)
    while len(matches) < number_of_drivers:
        # Initialize minimum distance to infinity for comparison
        min_dist = float('inf')
        # To keep track of the index of the best passenger for the current driver
        best_passenger = None
        # To keep track of the index of the best driver for the current passenger
        best_driver = None

        # Iterate through each passenger and driver to find the closest pair that has not been matched yet
        # 'enumerate' is used to get both the index and the passenger data from the passengers list
        for i, passenger in enumerate(passengers):
            if i in used_passengers:
                continue

            # For each passenger, iterate through the drivers list to find the closest driver that has not been matched yet
            for j, driver in enumerate(drivers):
                if j in used_drivers:
                    continue

                # Calculate the distance between the current passenger and driver using the 'distance' function defined in line 20
                dist = distance(passenger, driver)

                # If the calculated distance is less than the current minimum distance, update the minimum distance and store the indices of the best passenger and driver
                if dist < min_dist:
                    min_dist = dist
                    best_passenger = i
                    best_driver = j

        # If no valid passenger-driver pair is found, break the loop to avoid infinite iterations
        if best_passenger is None or best_driver is None:
            break

        used_passengers.add(best_passenger)
        used_drivers.add(best_driver)
        # Append the matched passenger and driver names and the distance to the matches list
        total_dist += min_dist
        matches.append(
            (
                passengers[best_passenger]['name'],
                drivers[best_driver]['name'],
                min_dist
            )
        )

    return matches, total_dist, used_passengers


# Call the greedy matching function and store the results in 'results' and 'total_dist' variables
results, total_dist, used_passengers = greedy_matching(passengers, drivers)

# Create a list of unmatched passengers by checking which passengers were not included in the used_passengers set
unmatched = [passengers[i]['name']
             for i in range(len(passengers)) if i not in used_passengers]


print("\nGreedy Matching Results:")
# Print the matched pairs of passengers and drivers along with the distance between them
for passenger, driver, dist in results:
    print(
        f"Passenger {passenger} is matched with Driver {driver} | Distance: {dist:.2f}")

# Print the total distance of all matches with 2 decimal places
print(f"Total distance = {total_dist:.2f}")

# Calculate and print the average distance of the matches, ensuring to handle the case where there are no matches to avoid division by zero
average_dist = total_dist / len(results) if results else 0
print(f"Average distance = {average_dist:.2f}")

# Print the list of unmatched passengers
print("\nUnmatched passengers (Greedy Matching):")
for name in unmatched:
    print(name)


# random matching of passengers and drivers using seed 42 for reproducibility
def random_matching(passengers, drivers):
    random.seed(42)  # Set a seed for reproducibility of random matches

    # Create a copy of the drivers list to shuffle without affecting the original list
    shuffled_drivers = drivers.copy()
    # random reordering of the items in drivers list, we could have used random.sample(drivers, len(drivers)) to achieve the same result without modifying the original list
    random.shuffle(shuffled_drivers)

    # Create a copy of the passengers list to shuffle without affecting the original list
    shuffled_passengers = passengers.copy()
    # random reordering of the items in passengers list
    random.shuffle(shuffled_passengers)

    matches = []  # an empty list that will store the result of passenger-driver pairing
    total_dist = 0  # set initial total distance to 0

    # loop through each driver and match with the corresponding passenger in the shuffled list
    for i in range(len(shuffled_drivers)):
        driver = shuffled_drivers[i]  # get driver at position i from list
        # get passenger at same position i from list
        passenger = shuffled_passengers[i]
        # calculate distance between passenger and driver using the distance function defined in line 20
        dist = distance(passenger, driver)
        matches.append({  # dictionary to store results of pairing
            'passenger': passenger['name'],
            'driver': driver['name'],
            'distance': dist
        })
        total_dist += dist  # calculate total distance

    # calculate average distance
    avg_distance = total_dist/len(shuffled_drivers)
    return matches, total_dist, avg_distance


# call function and separate its results to 3 variables
matches, total_distance, avg_distance = random_matching(passengers, drivers)

# printing the results of random matching
print("\nRandom Matching Results:")
for match in matches:  # a loop to print each passenger-driver match
    print(
        f"Passenger: {match['passenger']} - Driver: {match['driver']} - Distance: {match['distance']:.2f}")

print(f"Total Distance: {total_distance:.2f}")  # print total distance
print(f"Average Distance: {avg_distance:.2f}")  # print average distance


# Get matched passenger names from random matching
matched_passenger_names = {match['passenger'] for match in matches}

# Print unmatched passengers from random matching
print("\nUnmatched passengers (Random Matching):")
for p in passengers:
    if p['name'] not in matched_passenger_names:
        print(p['name'])


# Comparison of Greedy and Random Matching
print("\nComparison of Greedy and Random Matching:")
print(
    f"Greedy - Total Distance: {total_dist:.2f}")
print(
    f"Random - Total Distance: {total_distance:.2f}")
# The greedy algorithm typically produces a lower total distance because it always selects the closest available pair.
# However, it does not guarantee an optimal solution, since early local decisions may lead to suboptimal overall matching.


# Visualization of the locations of passengers and drivers, and the matches between them
# Create a figure and axis for plotting
fig, ax = plt.subplots(figsize=(10, 10))

# Set the limits of the plot to ensure all points are visible (coordinates are between 0 and 100)
ax.set_xlim(0, 100)  # Set x-axis limits
ax.set_ylim(0, 100)  # Set y-axis limits

# Set the title of the plot
ax.set_title("Ride-Sharing Matching: Passengers and Drivers")

ax.grid(True)  # Enable grid for better visibility of points

# Passengers
for p in passengers:
    # Plot passenger locations as blue circles
    ax.scatter(p['x'], p['y'], color='blue', s=50)
    # Annotate passenger names next to their locations
    ax.annotate(p['name'], (p['x'], p['y']),
                # xytext=(5, 6): shifts the label 5 points to the right and 6 points up from the marker, so it no longer overlaps
                xytext=(5, 6), textcoords='offset points',
                # textcoords='offset points': tells matplotlib those numbers are in points (screen units), not data coordinates, so the offset is consistent regardless of zoom level
                fontsize=7, color='blue')

# Drivers
for d in drivers:
    # Plot driver locations as red triangles
    ax.scatter(d['x'], d['y'], color='red', marker='^', s=70)
    # Annotate driver names next to their locations
    ax.annotate(d['name'], (d['x'], d['y']),
                xytext=(5, 6), textcoords='offset points',
                fontsize=7, color='red')

# Draw lines between matched passengers and drivers based on the results from the greedy matching
for passenger_name, driver_name, dist in results:
    # Find passenger coordinates by name
    p = next(p for p in passengers if p['name'] == passenger_name)
    # Find driver coordinates by name
    d = next(d for d in drivers if d['name'] == driver_name)
    # Draw a dashed line between matched passenger and driver
    ax.plot([p['x'], d['x']], [p['y'], d['y']], 'g--', linewidth=1, alpha=0.6)

plt.tight_layout()  # Adjust the layout to prevent overlap of elements in the plot
# Display the plot without blocking the execution of the next lines of code
plt.show(block=False)
# Pause to allow the plot to render before moving on to the next visualization
plt.pause(0.1)


# Visualization for Random Matching
fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_title("Ride-Sharing Matching: Random Matching")
ax.grid(True)

# Passengers
for p in passengers:
    ax.scatter(p['x'], p['y'], color='blue', s=50)
    ax.annotate(p['name'], (p['x'], p['y']),
                xytext=(5, 6), textcoords='offset points',
                fontsize=7, color='blue')

# Drivers
for d in drivers:
    ax.scatter(d['x'], d['y'], color='red', marker='^', s=70)
    ax.annotate(d['name'], (d['x'], d['y']),
                xytext=(5, 6), textcoords='offset points',
                fontsize=7, color='red')

# Draw lines between matched passengers and drivers based on random matching
for match in matches:
    p = next(p for p in passengers if p['name'] == match['passenger'])
    d = next(d for d in drivers if d['name'] == match['driver'])
    ax.plot([p['x'], d['x']], [p['y'], d['y']], 'g--', linewidth=1, alpha=0.6)

plt.tight_layout()
plt.show()
