# 1.Write a function that returns a float corresponding to the volume of a sphere:
print("-------Exercise 1:")

import math
def get_sphere_volume(radius):
    volume = (4/3) * math.pi * (radius**3)
    return float(volume)
print(get_sphere_volume(3))

print(" ")

# 2. Write a function that calculates and returns an integer corresponding to the factorial of an integer (n):
## 2A. Using recursivity:
print("-------Exercise 2A:")

def recursive_factorial(n):
    if n == 0 or n == 1: #we need a case to stop the recursion
        return 1
    else:
        return n * recursive_factorial(n - 1)
print(recursive_factorial(3))

print(" ")
## 2B. Without using recursivity:
print("-------Exercise 2B:")

def factorial(n):
    result = 1 #start from 1 because multiplying by 0 gives 0
    for i in range(1, n + 1):
        result *= i #the code repeats the multiplication for every number from 1 to n
        #result = result * i
    return result
print(factorial(3))
print(" ")

# 3. Write a function for counting up numbers from 0 to n, showing the count up in the screen. If parameter odd (imparell) is set to True, prints only odd numbers:
## 3A. Using recursivity:
print("-------Exercise 3A:")

def recursive_count_up(n, odd): #odd is a boolean parameter, when False shows all numbers, when True shows only odd numbers
    if n < 0:
        return #Stop calling itself once it reaches a negative number
    recursive_count_up(n - 1, odd)
    if odd: #Cheks whether we only want odd numbers
        if n % 2 != 0: #if the remainder is not 0, the number is odd
            print(n)
    else:
        print(n)

print("Showing all numbers:")
recursive_count_up(5, False)
print("Showing only the odd numbers:")
recursive_count_up(5, True)
print(" ")

## 3B. Without using recursivity: --> usage of for loop!!!!
print("-------Exercise 3B:")
def count_up(n, odd):
    if n < 0:
        return
    for i in range(n + 1):
        if odd:
            if i % 2 != 0:
                print(i) 
        else:
            print(i) #prints only when odd == False
print("Showing all numbers:")
count_up(3, False)
print("Showing only the odd numbers:")
count_up(3, True)
print(" ")

# 4. Find and solve the bugs in the following function:
print("-------Exercise 4:")
#def get_final_price(discount_percentage=10, price): 
 #   """Return the final price after applying the discount percentage """
  #  return ((price + price) * discount_percentage) / 100

## Corrected function:
def get_final_price(price, discount_percentage=10):
    """Return the final price after applying the discount percentage """
    discount = (price * discount_percentage) / 100
    final_price = price - discount
    return final_price

print(get_final_price(100))
print(get_final_price(36, 40))