# control structures in python : )
# if else statement that checks if a number is negative or positive 
def sign_check(number):
    if number > 0:
        print("Positive")
    elif number < 0:
        print("Negative")
    else:
        print("Number is 0")

# return prime numbers 
def prime_numbers(n):
    if n < 2:
        return False 
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# and then, here you make a loop to print the first 10 prime numbers 
def print_prime():
    prime = []
    for n in range(2,30):
        if len(prime) == 10:
            break
        if prime_numbers(n):
            prime.append(n)
            print(n)

#sum from 1 to 100 using a while loop 
def sum_hundred():
    total = 0 
    number = 1 

    while number <= 100:
        total += number 
        number += 1

    print(total)

