def bubble_sort(arr):
    n=len(arr)
    
    for a in range(n):
        for b in range(0,n-a-1):
            if arr[b]>arr[b+1]:
                arr[b],arr[b+1]=arr[b+1],arr[b]
                
    return arr

res=bubble_sort([64, 34, 25, 12, 22, 11, 90])
print(res)