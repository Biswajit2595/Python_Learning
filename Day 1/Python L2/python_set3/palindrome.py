def palin_Check(str):
    
    str=str.replace(" ","").lower()
    
    if str==str[::-1]:
        return f"The word {str} is a palindrome."
    else:
        return f"The word {str} is not a palindrome."
    

print(palin_Check("Racecar"))