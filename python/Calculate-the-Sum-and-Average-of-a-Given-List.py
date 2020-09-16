#!python

# Calculate the sum and average of a given list in Python
# =======================================================

sum = 0
list = [11,22,33,44,55,66,77]
for num in list:
  sum = sum +num
average  = sum / len(list)
print ("sum of list element is : ", sum)
print ("Average of list element is ", average )
