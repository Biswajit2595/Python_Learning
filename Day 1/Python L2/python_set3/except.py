def division(num1,num2):
    try:
        res=num1/num2
        return res
    except ZeroDivisionError:
        return "Cannot be divided by zero."
    

print(division(5,0))