def is_power_of_two(n):
    if n<=0:
        return False
    return (n & (n-1)) == 0

res=is_power_of_two(256)
print(res)