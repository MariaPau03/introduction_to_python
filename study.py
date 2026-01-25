# Collection = single "variabele" used to store mutliple values
    # List = [] ordered and changeable. Duplicates ok
fruits = ["apple", "orange", "bannana", "coconut"]
print(fruits)
print(fruits[3])
print(fruits[::2])
    ##iterate over my list
print("-" * 10)
for x in fruits:
    print(x)
    ##Each element of the list, is an element. 
print(dir(fruits)) # will print attributes
print("-" * 10)
print(len(fruits))


print("apple" in fruits)

fruits.append("melon")
fruits.sort()
#fruits.reverse() 
print(fruits)


# Set = () unordered and immutable (cannot alter this values), but Add/Remove ok. No duplicates
fruits = ("apple", "orange", "bannana", "coconut")
print(dir(fruits)) #to see the methods 
##CANNOT USE INDEXING BECAUSE THEY ARE UNORDERED!!
# Tuple = () ordered and unchangeable. Duplicates ok. FASTER
fruits = ("apple", "orange", "bannana", "coconut")
print("pineapple" in fruits)
print(fruits.index("apple"))
print(fruits.count("coconut"))
for fruit in fruits:
    print(fruits)



car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

x = car.values()

print(x)