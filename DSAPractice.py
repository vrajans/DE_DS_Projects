

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

#print(removeDuplicates([1,1,2]))

#print(reverse_arr([1, 2, 3, 4,7,9]))
# =======
#<<<<<<< HEAD
# print(reverse_arr([1, 2, 3, 4,7,9,8]))
# >>>>>>> e6ef39bdbc7ad2b9f01a7b9dc4d7676c145899b0
# =======
#=======

#print(reverse_arr([1, 2, 3, 4,7,9,8]))


def merge(nums1, m, nums2, n):
    nums1[m:] = nums2[:n]
    nums1.sort()
    return nums1

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
    
    i = 2
    if len(nums) > 2:
        for j in range(2, len(nums)):
            if nums[j] != nums[i-2]:
                nums[i] = nums[j]
                i += 1
        return i, nums[:i]
    return len(nums), nums

def majorityElement(nums):
    count = 0
    candidate = 0
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    return candidate

#print(majorityElement([3,2,3]))

#factorial of a number using recursion
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
    
#print(factorial(5))

#fibonacci series using recursion
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
    
#print(fibonacci(6))

#factorial of a number using iteration
def factorial_iter(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

#print(factorial_iter(5))

def varath_factorial(n):
    if n == 0 or n == 1:
        return 1
    
    result = 1  
    for i in range(1,n+1):
        result = result * i
    return result

#print(varath_factorial(5))


def varath_fibanaci(n):
    fib = []
    result = 0
    prev = 0
    cur = 0
    for i in range(n+1):
        result = prev + cur
        fib.append(result)
        if fib[i] == 0:
            prev = 0
            cur = 1
        else:
            prev = fib[i-1]
            cur = fib[i]

    return fib

#print(varath_fibanaci(6))

def is_str_plolyndrom(str):
    
    str_poly_chk = ""

    for c in reversed(str):
        str_poly_chk = str_poly_chk + c

    if str.upper() == str_poly_chk.upper():
        print("the given sting is polyndrom")
    else:
        print("the given string is not polyndrom")

is_str_plolyndrom("Malayalam")


def generate_primenumbers(n):
    prime_numbers = []
    for i in range(1, n+1):
        if ((i != 1 and i % 2 != 0) or i==2):
            if((i%3 != 0 or i==3) and (i%5 != 0 or i==5) and (i%7 != 0 or i==7)):
                prime_numbers.append(i)

    return prime_numbers

print(generate_primenumbers(200))