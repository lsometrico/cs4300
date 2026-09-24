default_file = "task6_read_me.txt"

def read_file_count(filename = default_file):
    with open(filename, "r") as file: 
        return len(file.read().split())

def main():
    print(f"The file contains {read_file_count()} words.")

if __name__ == "__main__":
    main()