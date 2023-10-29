# Initialized a empty dictionary which is similar to Objects in JS

dict={}

# Function to add key-value pair in the dictionary
def name_age(name,age):
    dict[name]=age

# Function to update the age in the dictionary
def age_update(name,age):
    if name in dict: # looping through the dictionary to check for the name and update the age of the name
        dict[name]=age
        
def name_del(name):
    if name in dict:
        del dict[name] # Delete the name if it exists in the dictionary
    else:
        print(f"{name} not found in the dictionary") # Incase the name is not present in the dictionary
        
print(f"{dict} --> printing the intial dictionary")


# Adding name and Age
name_age("Jim",32)
print(f"{dict} --> adding name and age")

#Updating Age
age_update("Jim",29)
print(f"{dict} --> updating age from {32} to {29}")

#Deleting with wrong name
name_del("John")

# Deleting from dictionary
name_del("Jim")
print(f"{dict} --> After deleting a name")

