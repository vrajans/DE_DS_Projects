

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

<<<<<<< HEAD
<<<<<<< HEAD
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
=======
print(reverse_arr([1, 2, 3, 4,7,9,8]))
>>>>>>> e6ef39bdbc7ad2b9f01a7b9dc4d7676c145899b0
=======
def merge(nums1, m, nums2, n):
    nums1[m:] = nums2[:n]
    nums1.sort()
    return nums1
>>>>>>> ba1c054bdadf2f7dfaadbd94fa7140d0aed46ae2

def removeElement(nums, val):
    while val in nums:
        nums.remove(val)
    return len(nums)


def removeDuplicates(nums):
    if not nums:
        return 0
    
    i = 0  # slow pointer
    for j in range(1, len(nums)):
        if nums[j] != nums[i]:  # found a new unique
            i += 1
            nums[i] = nums[j]
    return i + 1

def removeDuplicates_2(nums):
    if not nums:
        return 0
    
    i = 0  # slow pointer
    if len(nums) > 2:        
        for j in range(1, len(nums)):
            if nums[j] != nums[i]:  # found a new unique
                i += 1
                nums[i+1] = nums[j]
        return i + 2, nums[:i+2]
    return len(nums), nums


print(removeDuplicates_2([1,2,3]))