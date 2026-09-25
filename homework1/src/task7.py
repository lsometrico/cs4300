# numpy for the last task; do the following to install: 
# pip install numpy 
import numpy as np 

# for this we just do basic stats and array math 
# return the dot product of two equal length lists 
def dot_product(a,b):
    return float(np.dot(np.array(a), np.array(b)))

# return mean, median & standard deviation of a list 
def stats_summary(values):
    arr = np.array(values, dtype = float)
    return{
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std dev": float(np.std(arr))
    }

def main():
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    print("Stats:", summary_stats(data))
    print("Dot product:", dot_product([1, 2, 3], [4, 5, 6]))


if __name__ == "__main__":
    main()