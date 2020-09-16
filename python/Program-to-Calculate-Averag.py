#!python

# Python Program to calculate average
# ===================================

print ("calculate an average of first n natural numbers\n")
n = input("Enter Number ")
n = int (n)
average = 0
sum = 0
for num in range(0,n+1,1):
  sum = sum+num;
average = sum / n
print("Average of first ", n, "number is: ", average)
