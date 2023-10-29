def permutions(str):
    if len(str) <=1:
        return [str]
    
    permute=[]
    
    for a,char in enumerate(str):
        for perm in permutions(str[:a] + str[a+1:]):
            permute.append(char + perm)
            
    return permute;


res=permutions("abc")
print(res)