import connect
import user
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


def checkcolor(style):
    return style == "color: rgb(51, 153, 0); font-family: Verdana;"


def checkposition(positionName, positionVoted):
    return positionName['y'] < positionVoted['y']


def check(browser, translator):
    correctTranslationList = ""
    incorrectTranslationList = ""
    incorrectTranslationTranslatorList = ""

    # Openning tasks
    file = open("tasks/tmp_tasks.txt", "r")
    tasks = file.read()
    tasks = tasks.split("\n")

    for task in tasks:

        print ('>> Task ID: ' + task)

        internalTaskURL = 'http://sofi.india.endurance.com/translator/filter?d1=0&d2=0&pt=1&pv=1&pid=3&pp=10&view=translation&tid=' + task + '&lc=pt-PT'

        try:
            browser.set_page_load_timeout(15)
            browser.get(internalTaskURL)

        except TimeoutException as ex:
            print("Timeout " + str(ex))

            # 1. Reload 1
            sourceText = browser.find_elements_by_xpath("//*[contains(text(), 'Text to Translate')]")
            if len(sourceText) == 0:
                print("Error: GET Fail, Reload attempt 1")
                browser.set_page_load_timeout(15)
                browser.get(internalTaskURL)

            # 2. Reload 2
            sourceText = browser.find_elements_by_xpath("//*[contains(text(), 'Text to Translate')]")
            if len(sourceText) == 0:
                print("Error: GET Fail, Reload attempt 2")
                browser.set_page_load_timeout(15)
                browser.get(internalTaskURL)

            # 3. Reconnect
            sourceText = browser.find_elements_by_xpath("//*[contains(text(), 'Text to Translate')]")
            if len(sourceText) == 0:
                print("Error: Connect connection attempt fail")
                print ("Trying to reconnect")
                browser.set_page_load_timeout(59)

                browser = connect.connectSofi(webdriver, user)

                if browser.current_url == "http://sofi.india.endurance.com/translator/filter":
                    print ("Connection successful!\n")
                    browser.get(internalTaskURL)

            # 4. Reload 3
            sourceText = browser.find_elements_by_xpath("//*[contains(text(), 'Text to Translate')]")
            if len(sourceText) == 0:
                print("Error: Reconnect fail, Reload attempt 3")
                browser.set_page_load_timeout(15)
                browser.get(internalTaskURL)

            sourceText = browser.find_elements_by_xpath("//*[contains(text(), 'Text to Translate')]")
            if len(sourceText) > 0:
                print("Connection restablished")

            # 5. Abort
            else:
                print("Error: Connection can not be established, abort.")
                sys.exit()



        elementVote = browser.find_elements_by_xpath("//*[contains(text(), 'Voted by')]")
        elementName = browser.find_elements_by_xpath("//*[contains(text(), '" + translator + "')]")
        # elementNameClass = browser.find_elements_by_class_name("sideTranslatorList")


        # Finding the correct translator name in the page
        if len(elementName) > 0 and len(elementVote) > 0:
            if elementName[0] and elementVote[0]:
                if checkposition(elementName[0].location, elementVote[0].location):
                    print ("=> Finding the first correct translator name in the page: ")
                    print ("  -> First translator name found upper,")

                    if len(elementName) > 1:
                        if checkposition(elementName[1].location, elementVote[0].location):
                            print ("    -> Second translator name found upper,")

                            if len(elementName) > 2:
                                print ("= Third translator found in the correct position, correct one.")
                                elementName = elementName[2:]
                            else:
                                print("= Any translation found in the right position, cleaning list.")
                                elementName = elementName[2:]

                        else:
                            print ("= Second translator found in the correct position, delete first one.")
                            elementName = elementName[1:]
                    else:
                        print("= Any translation found in the right position, cleaning list.")
                        elementName = elementName[1:]

                else:
                    print("[First translator name in the right position]")
            else:
                print("[No vote or name found]")
        else:
            if len(elementName) == 0:
                print("Name not found")
            else:
                print("Voted by not found")

        print ('Translator name found: ' + str(len(elementName)))
        print ('Voted by found: ' + str(len(elementVote)))

        if len(elementVote) == 0:

            incorrectTranslationTranslatorList = incorrectTranslationTranslatorList + str(task) + " - No translation found\n"

            print ("No translation found")
            print ("Incorrect Translator Translation\n")

        elif len(elementVote) == 1 and len(elementName) == 1:

            status = checkcolor(elementName[0].get_attribute('style'))

            if status:
                correctTranslationList = correctTranslationList + str(task) + "\n"
                print ("One translation found - Correct color")
                print ("Correct Translation\n")

            else:
                incorrectTranslationTranslatorList = incorrectTranslationTranslatorList + str(task) + " - One translation found - Incorrect color\n"
                print ("One translation found - Incorrect color")
                print ("Incorrect Translator Translation\n")

        else:
            if len(elementName) == 0:
                incorrectTranslationTranslatorList = incorrectTranslationTranslatorList + str(task) + " - No translation from " + translator + " found\n"
                print ("No translation from " + translator + " found")
                print ("Incorrect Translator Translation\n")

            elif len(elementName) > 0 and len(elementVote) > 0:
                status = checkcolor(elementName[0].get_attribute('style'))
                status2 = checkposition(elementName[0].location, elementVote[1].location)

                if status and status2:
                    correctTranslationList = correctTranslationList + str(task) + "\n"
                    print ("Multiple translations found - Color and position correct")
                    print ("Correct Translation\n")

                else:
                    status3 = False
                    for element in elementName:
                        if checkcolor(element.get_attribute('style')):
                            status3 = True

                    if status3:
                        incorrectTranslationList = incorrectTranslationList + str(task) + "\n"
                        print ("Multiple translations found - Position: " + str(status2) + " Color: " + str(status))
                        print ("Incorrect Translation\n")

                    else:
                        incorrectTranslationTranslatorList = incorrectTranslationTranslatorList + str(task) + " - Any green translation from " + translator + " found\n"
                        print ("Any green translation from " + translator + " found")
                        print ("Incorrect Translator Translation\n")


            else:
                print("Error!")

                print("Element Vote:")
                for i in elementVote:
                    print (i, len(elementVote))

                print ("Element Name:")
                for j in elementName:
                    print (j, len(elementName))

                file = open("tasks/errors.txt", "a")
                file.write(str(task) + "\n")
                file.close()

    print ("Correct Translations for this batch:\n" + correctTranslationList)
    if correctTranslationList == "":
        print ("None")
    print ("\nIncorrect Translations for this batch:\n" + incorrectTranslationList)
    if incorrectTranslationList == "":
        print ("None")
    print ("\nIncorrect Translator Translations for this batch:\n" + incorrectTranslationTranslatorList)
    if incorrectTranslationTranslatorList == "":
        print ("None")

    # Remove empty lines in the end
    # if correctTranslationList != "":
    #    correctTranslationList = correctTranslationList[:-1]

    # if incorrectTranslationList != "":
    #   incorrectTranslationList = incorrectTranslationList[:-1]

    file = open("tasks/tmp_correct.txt", "w")
    file.write(correctTranslationList)
    file.close()

    file = open("tasks/tmp_incorrect.txt", "w")
    file.write(incorrectTranslationList)
    file.close()

    file = open("tasks/incorrect_translator.txt", "a")
    file.write(incorrectTranslationTranslatorList)
    file.close()
