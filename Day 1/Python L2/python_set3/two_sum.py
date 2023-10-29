list=[2,7,11,15]

def two_sum(arr,target):
    left=0
    right=len(arr)-1

    while left<right:
        if arr[left]+arr[right]==target:
            return [left,right]
        elif arr[left]+arr[right]<target:
            left+=1
        else:
            right-=1
    return [-1,-1]
print(two_sum(list,9))