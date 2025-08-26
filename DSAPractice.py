

def max_arr(arr):
    max_val = arr[0]
    for val in arr:
        if val>max_val:
            max_val = val
    return  max_val

def count_even_numbers(arr):
    even_num_count = 0
    for val in arr:
        if val%2 == 0:
            even_num_count = even_num_count + 1
    return even_num_count

def reverse_arr(arr):
    arr_len = len(arr)
    arr_new = arr.copy()
    for i, val in enumerate(arr_new):
        arr_len = arr_len - 1
        if arr_len >= 0:
            arr[arr_len] = val
    return arr

def merge(nums1, m, nums2, n):
    nums1[m:] = nums2[:n]
    nums1.sort()
    return nums1

def removeElement(nums, val):
    while val in nums:
        nums.remove(val)
    return len(nums)


def removeDuplicates(nums):
    seen = set(nums)
    return  len(seen)


print(removeDuplicates([0,0,1,1,1,2,2,3,3,4]))