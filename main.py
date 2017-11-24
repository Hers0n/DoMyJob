from selenium import webdriver

import form
import user
import connect


def contructTaskFiles(browser, translator, tasksLoop, tasksperloop):

    # Injecting tasks in tmp_tasks
    file = open("tasks/tmp_tasks.txt", "w")
    insertStr = ""
    for taskLine in range(tasksperloop):
        if taskLine != tasksperloop - 1:
            insertStr = (insertStr + str(tasksLoop[taskLine]) + "\n")
        else:
            insertStr = (insertStr + str(tasksLoop[taskLine]))
    file.write(insertStr)
    file.close()

    # Run
    form.check(browser, translator)

    # Read results and update correct.txt and incorrect.txt
    file = open("tasks/tmp_correct.txt", "r")
    read = file.read()

    file = open("tasks/correct.txt", "a")
    file.write(read)
    file.close()

    file = open("tasks/tmp_incorrect.txt", "r")
    read = file.read()

    file = open("tasks/incorrect.txt", "a")
    file.write(read)
    file.close()


print ("DoMyJob 2.0 \n============\n")

# Getting Tasks
file = open("tasks/tasks.txt", "r")
tasks = file.read()
tasks = tasks.split("\n")

# Remove empty lines
while '' in tasks:
    tasks.remove('')

print ("Translator: " + user.translator)
print ("Total Tasks: " + str(len(tasks)))

tasksperloop = input("Tasks per loop: ")
tasksperloop = int(tasksperloop)

# Translations per loop
loops = int(len(tasks) / tasksperloop)
finalLoop = int(len(tasks) % tasksperloop)

if finalLoop == 0:
    print ("Loops: " + str(loops))
else:
    print ("Loops: " + str(loops + 1))
    print ("Tasks for the last loop: " + str(finalLoop))
print ("Tasks per Loop: " + str(tasksperloop))


print ("\nConnecting to Sofi...")
browser = connect.connectSofi(webdriver, user)

if browser.current_url == "http://sofi.india.endurance.com/translator/filter":
    print ("Connection successful!\n")

    for loop in range(loops):
        # Take the tasks for this loop
        tasksLoop = tasks[:tasksperloop]

        # Update general tasks without first elements
        tasks = tasks[tasksperloop:]

        contructTaskFiles(browser, user.translator, tasksLoop, tasksperloop)

    # Elements for last loop
    contructTaskFiles(browser, user.translator, tasks, finalLoop)

    print ("End.")

else:
    print ("\nConnection Error!")