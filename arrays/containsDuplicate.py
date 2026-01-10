# You’re scanning numbers. If any number appears more than once → return True, else False.

def containsDuplicate(nums):
    seen = set() # existence
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

print(containsDuplicate([1,2,3,4,5,6,7,7,9,10]))