# name the file to be read by the script 
default_file = "task6_read_me.txt"

#and then count the number of splits in the file & print in main 
def read_file_count(filename = default_file):
    with open(filename, "r") as file: 
        return len(file.read().split())

def main():
    print(f"The file contains {read_file_count()} words.")

if __name__ == "__main__":
    main()