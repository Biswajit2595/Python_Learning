def contains_duplicate(arr):
    n=len(arr)
    for a in range(n):
        for b in range(a+1,n):
            if arr[a]==arr[b]:
                return True
            
        return False
    
#     unique_set=set()
#     for a in arr:
#         if a in unique_set:
#             return True
#         unique_set.add(a)
        
#     return False

    
res=contains_duplicate([1,2,3,1])
print(res)