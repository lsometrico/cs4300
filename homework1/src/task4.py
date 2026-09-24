# if it walks like a duck, sounds like one and swims like one it probably is a duck
# ducktyping in this example are any numeric type that support operations, be it int, float, etc 

def calc_discount(price, discount):
    return price - (price / discount / 100)

def main():
    print(calc_discount(100, 40))
    print(calc_discount(59.99,15.5))

if __name__ == "__main__":
    main()