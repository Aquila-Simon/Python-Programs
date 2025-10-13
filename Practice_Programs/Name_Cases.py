#USE A VARIABLE TO REPRESENT A PERSON'S NAME AND PRINT A MESSAGE EX: "Hello Eric, would you like to learn some python today?"
name="Karina"
Intro=f"Hello {name},"
Question="do you like Apples?"
Full_message=f"{Intro} {Question}"
print(Full_message)
#OR ALTERNATIVELY
name="Karina"
print(f"Hello {name}, do you like Apples?")

#USE A VARIABLE TO REPRESENT A PERSON'S NAME, AND THEN PRINT THAT PERSON'S NAME IN LOWERCASE, UPPERCASE, AND TITLE CASE
name="simon villanueva"
print(name.lower())
print(name.upper())
print(name.title())

#FIND A QUOTE FROM A FAMOUS PERSON YOU ADMIRE. PRINT THE QUOTE AND THE NAME OF THE AUTHOR, OUTPUT SHOULD LOOK LIKE THIS INCLUDING QUOTATION MARKS
#Albert Einstein once said, "A person who never made a msitake never tried anything new."
print('Ysabella Dejecacion once said, "At the end of the day, gabi na."')

#REDO LAST EXERCISE BUT USING VARIABLES famous_person and message to write person's name and the whole message
famous_person="ysabella dejecacion"
message='"At the end of the day, gabi na."'
print(f"{famous_person.title()} once said, {message}")

#USE A VARIABLE TO WRITE A PERSON'S NAME WITH WHITESPACE ON BOTH SIDES. USING \t and \n accordingly to show no whitespace fix,
#.lstrip(), .rstrip(), and .strip()
name=" simon villanueva "
print("\t",name.lstrip(),"\n\t",name.rstrip(),"\n\t",name.strip())

#PYTHON HAS A removesuffix() method that is similar to removeprefix(). ASSIGN THE VALUE 'python_note.txt' to a variable called filename.
#DISPLAY filename without the file extension
filename='python_note.txt'
print(f"Before removesuffix(), {filename}")
print(f"After removesuffix(), {filename.removesuffix(".txt")}")