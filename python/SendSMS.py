import subprocess

# Add Entries to the address book dictionary. Key = Name, Value = Phone Number
addressbook= {"Amazon Shipping" : "262966"
		"Amber Lemon" : "7173068527"
		"April Lemon" : "7172716642"
		"Cindy Young" : "7174090086"
		}
# Loop through the addressbook dictionary and send each number the message
for (k,v) in addressbook.items():
    
    # SMS Message Template (try to keep to within 150 characters)
    smsmessage = str("Hi " + k + "7" + v)
    
    # Use Subprocess Run Function to send SMS
    subprocess.run(["termux-sms-send", "-n", phonenumber, smsmessage])
    
    # Print confirmation of each send
    print("Sent Message to " + k + " via " + v)


# Print end of process message

print("Message sending complete")

# Save the python script and exit nano by pressing CTRL+X in Nano

python sendsms.py
