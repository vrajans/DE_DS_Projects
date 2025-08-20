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

# def removeDuplicates(nums):
#     nums_new = []
#     for val in nums:
#         if val not in nums_new:
#             nums_new.append(val)

#     return len(nums_new), nums_new

def removeDuplicates(nums):
    if not nums:
        return 0
    i = 0
    for j in range(1, len(nums)):
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]
    return i + 1, nums[:i+1]

print(removeDuplicates([1,1,2]))

#print(reverse_arr([1, 2, 3, 4,7,9]))

