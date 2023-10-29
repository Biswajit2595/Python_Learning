def anagram_Check(str1,str2):
    str1=str1.replace(" ","").lower()
    str2=str2.replace(" ","").lower()
    
    
    return sorted(str1)==sorted(str2)


res=anagram_Check("cinema","iceman")
print(res)