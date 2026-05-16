import random
import time
import statistics
import matplotlib.pyplot as plt
import sys

# MERGE SORT
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# QUICK SORT
# LAST ELEMENT PIVOT
# Best Case: balanced partitions
# Worst Case: sorted/reverse sorted arrays
def quick_sort(arr):
    quick_sort_recursive(arr, 0, len(arr) - 1)


def quick_sort_recursive(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)

        quick_sort_recursive(arr, low, pivot_index - 1)
        quick_sort_recursive(arr, pivot_index + 1, high)


def partition(arr, low, high):
    pivot = arr[high]

    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


# DATASET GENERATORS
def generate_sorted(n):
    return list(range(n))


def generate_reverse_sorted(n):
    return list(range(n, 0, -1))


def generate_random(n):
    return [random.randint(0, n) for _ in range(n)]


def generate_nearly_sorted(n):
    arr = list(range(n))

    swaps = max(1, n // 20)  # 5% disorder

    for _ in range(swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]

    return arr


# TIMING FUNCTION
def measure_time(sort_function, arr, repetitions):
    execution_times = []

    for _ in range(repetitions):
        test_arr = arr.copy()

        start = time.perf_counter()

        if sort_function.__name__ == "merge_sort":
            sort_function(test_arr)
        else:
            sort_function(test_arr)

        end = time.perf_counter()

        execution_times.append((end - start) * 1000)

    return statistics.mean(execution_times)


# EXPERIMENT SETTINGS
print("\n========== SORTING ALGORITHM ANALYSIS ==========\n")

# USER INPUTS
try:
    repetitions = int(input("Enter number of repetitions (5-10 recommended): "))
except:
    repetitions = 5

print("\nChoose Input Sizes:")
print("1. Default Sizes")
print("2. Custom Sizes")

choice = input("Enter choice: ")

if choice == "2":
    sizes_input = input(
        "Enter sizes separated by commas (example: 1000,2000,5000): "
    )
    sizes = [int(x.strip()) for x in sizes_input.split(",")]
else:
    sizes = [1000, 2000, 5000, 10000, 20000]

# Prevent recursion depth crash for worst-case quicksort
sys.setrecursionlimit(300000)

# CASE DEFINITIONS
cases = {
    "Best Case": generate_random,
    "Worst Case": generate_sorted,
    "Average Case": generate_random
}

# RUN EXPERIMENTS
results = {}

for case_name, generator in cases.items():

    merge_times = []
    quick_times = []

    print(f"\nRunning {case_name}...")

    for n in sizes:
        print(f"Testing n = {n}")

        dataset = generator(n)

        # MERGE SORT
        merge_time = measure_time(
            merge_sort,
            dataset,
            repetitions
        )

        # QUICK SORT
        quick_time = measure_time(
            quick_sort,
            dataset,
            repetitions
        )

        merge_times.append(merge_time)
        quick_times.append(quick_time)

        print(
            f"Merge Sort: {merge_time:.4f} ms | "
            f"Quick Sort: {quick_time:.4f} ms"
        )

    results[case_name] = {
        "merge": merge_times,
        "quick": quick_times
    }

# GRAPH PLOTTING
for case_name in results:

    plt.figure(figsize=(10, 6))

    plt.plot(
        sizes,
        results[case_name]["merge"],
        marker='o',
        label='Merge Sort'
    )

    plt.plot(
        sizes,
        results[case_name]["quick"],
        marker='s',
        label='Quick Sort'
    )

    plt.title(f"{case_name} Running Time Comparison")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (ms)")
    plt.legend()
    plt.grid(True)

    plt.show()

# SUMMARY OUTPUT
print("\n========== SUMMARY ==========\n")

print("1. Merge Sort:")
print("- Time Complexity:")
print("  Best Case    : O(n log n)")
print("  Average Case : O(n log n)")
print("  Worst Case   : O(n log n)")
print("- Stable sorting algorithm.")
print("- Performance remains consistent across datasets.\n")

print("2. Quick Sort:")
print("- Time Complexity:")
print("  Best Case    : O(n log n)")
print("  Average Case : O(n log n)")
print("  Worst Case   : O(n^2)")
print("- Usually faster in practice.")
print("- Performs poorly on sorted data using last-element pivot.\n")

print("3. Experimental Observation:")
print("- Merge Sort should show stable graph growth.")
print("- Quick Sort should perform well on random data.")
print("- Quick Sort worst-case graph will rise sharply.")
print("- Larger input sizes amplify the difference.\n")