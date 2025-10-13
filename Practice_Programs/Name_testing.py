name = "simon villanueva"
print(name.title()) #.title() is called a method. Each method is always followed by a set of parenthesis
print("\n")
print(name.upper())
print(name.lower())
print("\n") #Adds Whitespace to Code \n adds new line \t adds tab

first_name="simon"
last_name="villanueva"
full_name=f"{first_name} {last_name}" #Formatting. A set of parenthesis is needed around Variables used in a string
print(full_name)
print(full_name.title())
print("\n")
print(f"Hello, {full_name.title()}!")
print("\n")
message=f"Hello, {full_name.title()}!"
print(message)

favourite_language="python "
favourite_language=favourite_language.rstrip() #REMOVES WHITESPACE FROM RIGHT SIDE
print(favourite_language)
favourite_language=" python"
favourite_language=favourite_language.lstrip() #REMOVES WHITESPACE FROM LEFT SIDE
print(favourite_language)
favourite_language=" python "
favourite_language=favourite_language.strip() #REMOVES WHITESPACE FROM BOTH SIDES
print(favourite_language)

google_url="https://google.com"
simple_url=google_url.removeprefix("https://") #REMOVES PREFIX BASED ON WHAT IS INSIDE PARENTHESIS
print(simple_url)