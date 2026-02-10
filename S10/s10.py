while True:

    try:
        x = int(input("Please enter a number:"))
        break

    except (ValueError, TypeError):
        print("Oops! That was not a valid number.Try again…") 