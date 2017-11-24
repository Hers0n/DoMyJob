file = open("text.txt", "r")

new_file = file.read()
new_file = new_file.replace("\n", " ")

file = open("text.txt", "w")

file.write(new_file)
file.close()