def select_sort(arr):
    n=len(arr)
    for a in range(n):
        min_ind=a
        for b in range(a+1,n):
            if arr[b]<arr[min_ind]:
                min_ind=b
                
        arr[a],arr[min_ind]=arr[min_ind],arr[a]
    return arr
                

print(select_sort([12, 7, 1, 15]))