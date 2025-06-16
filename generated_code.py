# Get user input
s = input("Enter a string: ")

# Process the string: lowercase and remove spaces
processed = s.lower().replace(" ", "")

# Check if the processed string is the same forwards and backwards
if processed == processed[::-1]:
    print("Yes")
else:
    print("No")