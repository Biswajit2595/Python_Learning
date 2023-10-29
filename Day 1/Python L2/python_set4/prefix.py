def longest_common_prefix(str):
    min_len=min(len(s) for s in str)
    prefx=""
    
    for a in range(min_len):
        char=str[0][a]
        for s in str:
            if s[a]!=char:
                return prefx
        prefx += char
        
    return prefx

res=longest_common_prefix(["flower", "flow", "flight"])
print(res)