import random, string

def generate_password(min_length, numbers=True,special_chars=True): #def is a function, format is "def [Name of Function](parameters that is needed when calling function)"
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters #Sets variable 'characters' to all available characters
    if numbers:
        characters += digits #Sets variable 'characters' to all available characters plus all available numbers
    if special:
        characters += special #Sets variable 'characters' to all available characters plus all available numbers plus all special characters

    pwd = '' 
    criteria_met = False
    has_numbers = False
    has_special_chars = False
    #Lines 14-17 initializes parameters that will generate password

    while not criteria_met or len(pwd) < min_length: #Generates password and limits it to minimum length that is input by user or if criteria is met meaning it has numbers and special characters if they are chosen
        new_chars = random.choice(characters)
        pwd += new_chars 

        if new_chars in digits:
            has_numbers = True
        if new_chars in special:
            has_special_chars = True

        criteria_met = True
        if numbers:
            criteria_met = has_numbers
        if special_chars:
            criteria_met = criteria_met and has_special_chars

    return(pwd) #Returns generated password

min_length = int(input('Please input password lenght needed (Numbers Only): ')) #Requires that input is an interger, if not then the process will return ValueError and stop the process
numbers = input("Use numbers in the password (y/n)? ").lower == 'y' #Writes input to be lowercase to be compared to determine if its true or false
special_chars = input('Use special characters in the password (y/n)? ').lower == 'y' #Writes input to be lowercase to be compared to determine if its true or false
#Lines 37-39 just asks for input from user


pwd = generate_password(min_length, numbers, special_chars) #Calls function along with parameters and assigns it to a variable
print(f'Generated password based on Input: {pwd}') #Prints out generated password based on input parameters
