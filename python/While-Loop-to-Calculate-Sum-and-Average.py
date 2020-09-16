#!python

# Python while loop to calculate sum and average
# ==============================================

n = 20
total_numbers = n
sum=0
while (n >= 0):
   sum += n
n-=1
print ("sum using while loop ", sum)
average  = sum / total_numbers
print("Average using a while loop ", average)
