import math
import time

# Radius of Earth in km
R = 6371


# Airport class
class Airport:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon


# Haversine distance
def haversine(a1, a2):
    lat1, lon1 = math.radians(a1.lat), math.radians(a1.lon)
    lat2, lon2 = math.radians(a2.lat), math.radians(a2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


# Brute force method
def brute_force(points):
    min_dist = float('inf')
    pair = None
    distances = []

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = haversine(points[i], points[j])
            distances.append((points[i].name, points[j].name, d))
            if d < min_dist:
                min_dist = d
                pair = (points[i], points[j])

    return min_dist, pair, distances


# Strip closest
def strip_closest(strip, d):
    min_dist = d
    pair = None

    strip.sort(key=lambda x: x.lat)

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j].lat - strip[i].lat) >= min_dist:
                break

            dist = haversine(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                pair = (strip[i], strip[j])

    return min_dist, pair


# Divide and conquer utility
def closest_util(points):
    if len(points) <= 3:
        min_dist, pair, _ = brute_force(points)
        return min_dist, pair

    mid = len(points) // 2
    mid_point = points[mid]

    dl, pair_l = closest_util(points[:mid])
    dr, pair_r = closest_util(points[mid:])

    if dl < dr:
        d = dl
        pair = pair_l
    else:
        d = dr
        pair = pair_r

    strip = [p for p in points if abs(p.lon - mid_point.lon) < d]
    d_strip, pair_strip = strip_closest(strip, d)

    if pair_strip is not None and d_strip < d:
        return d_strip, pair_strip

    return d, pair


# Main function
def closest_pair(airports):
    points = sorted(airports, key=lambda x: x.lon)
    return closest_util(points)


# Sample data
airports = [
    Airport("Delhi", 28.5562, 77.1000),
    Airport("Mumbai", 19.0896, 72.8656),
    Airport("Chennai", 12.9941, 80.1709),
    Airport("Bangalore", 13.1986, 77.7066),
    Airport("Kochi", 10.1520, 76.4019),
    Airport("Hyderabad", 17.2403, 78.4294)
]


# Execution
start = time.time()

min_dist, pair = closest_pair(airports)
_, _, all_distances = brute_force(airports)

end = time.time()


# Output formatting
output = []

output.append("AIRPORT LIST:\n")
for a in airports:
    output.append(f"{a.name}: ({a.lat}, {a.lon})")

output.append("\nDISTANCES:")
for d in all_distances:
    output.append(f"{d[0]} - {d[1]} = {d[2]:.2f} km")

output.append("\nCLOSEST PAIR:")
output.append(f"{pair[0].name} and {pair[1].name}")
output.append(f"Minimum Distance = {min_dist:.2f} km")

output.append("\nTIME COMPLEXITY:")
output.append("O(n log n)")
output.append(f"\nExecution Time: {end - start:.6f} seconds")


# Print output
for line in output:
    print(line)


# Save to file
with open("closest_airports_output.txt", "w") as f:
    for line in output:
        f.write(line + "\n")

print("\nOutput saved to 'closest_airports_output.txt'")
