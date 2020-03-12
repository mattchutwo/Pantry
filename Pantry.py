import re  # re, sys module
from sys import exit  # imports exit method from system module

import bcrypt

import am  # separate methods am.py
import e  # AES encryption for user data from e. py


def StartMenu():
    """
    Leads the user to the main menu or exit;
    prompts user creation or login based of the existance of d.txt

    """

    global accWeb, accUser, accPass  # global variables for data
    am.Abyss()
    print("Welcome to Pantry".center(35, ' ') + "\n")
    am.Abyss()

    # List initialization for the user's accounts
    # All are correspondant to index's
    accWeb = []  # WEBSITES
    accUser = []  # USERNAMES
    accPass = []  # PASSWORDS

    # Checks if it is a first time run
    if not am.CheckFileExists("d.txt"):
        SetmName()
        SetmPass()
        MainMenu()

    # if d.txt exits...
    # login/exit menu
    print("Enter the number coresponding to desired feature:\n\n",
          "1)Log-In\n",
          "2)Exit\n")

    # while loop for user input
    while True:
        try:
            uChoice = int(input())
            if uChoice in range(1, 3):
                break
            else:
                print("Please only enter numbers")
        except ValueError:
            print("Please only enter numbers")

    if uChoice == 1:
        LogIn()
    if uChoice == 2:
        End()


def SetmName():
    """
    Get's user's name from user
    mName = input(name)
    """
    global mName
    while True:
        mName = input("Please enter a name using only letters\n - ")
        if not re.match("[a-z,A-Z]*$", mName):
            print("Only letters please")
            continue
        else:
            am.Abyss()
            break


def SetmPass():
    """
    # Method to set the Master Password used for login authentication
    # Validates the given password based off of the standards
    """
    global mPass

    while True:
        flag = 0  # Problem Counter
        print(
            "Your master password must:\n\t- Contatin 8-16 characters\n\t- Contain at least 1 Lowercase letter\n\t- "
            "Contain at least 1 Uppercase letter\n\t- Contain at least 1 number\n\t- Contain at least 1 special "
            "character(!@#$)\n")
        mPass = input("Input master password: \n - ")

        if len(mPass) < 8:
            print("Must be at least 8 characters\n")
            flag = -1

        if len(mPass) > 16:
            print("Must be shorter than 16 characters\n")
            flag = -1

        if ' ' in mPass:
            print("Cannot contain spaces")
            flag = -1

        if not re.search("[0-9]", mPass):
            print("Must contain a number")
            flag = -1

        if not re.search("[A-Z]", mPass):
            print("Must contain at least 1 uppercase letter")
            flag = -1

        if not re.search("[!@#$]", mPass):
            print("Must contain at least 1 special character")
            flag = -1

        if not re.search("[a-z]", mPass):
            print("Must contain at least 1 lowercase letter")
            flag = -1

        if flag == 0:
            break

        else:
            print("Please make sure your master password follows our requirements")


def Export():
    """
    Exports user data to d.txt

    """
    global mName, mPass, accWeb, accUser, accPass, key

    # open and write to file d.txt
    with open("d.txt", "w") as f:
        f.write("{}\n{}\n".format(mName, bcrypt.hashpw(mPass.encode(), bcrypt.gensalt(16)).decode(
            'utf-8')))  # string format to fill line 0 & 1
        if len(accWeb) != 0:  # Condition to write only if there is present data
            for i in range(len(accWeb)):  # Loop to write individual account data in each line
                f.write("{}:{}:{}\n".format(e.Encrypt(accWeb[i], key), e.Encrypt(accUser[i], key),
                                            e.Encrypt(accPass[i], key)))  # format : website:username:password


def Import():
    """
    Imports user data from d.txt

    """
    global accWeb, accUser, accPass, mPass, mName, key
    # open and read file d.txt
    with open("d.txt", "r") as f:
        lineList = f.readlines()
        mName = lineList[0]  # first line, user name
        mPass = lineList[1]  # second line, master password hash
        if len(lineList) == 2:  # length condition upon present data
            return
        else:
            for i in range(2, len(lineList)):
                t = lineList[i].split(":") # splits the read line
                accWeb.append(str(e.Decrypt(lineList[i], key))[2:-1]) # appends account data to each respective list
                accUser.append(str(e.Decrypt(lineList[i], key))[2:-1])
                accPass.append(str(e.Decrypt(lineList[i], key))[2:-1])


def LogIn():
    """
    Log-in prompt to verify user through password authentication

    """
    global mPass, key
    #open and read file d.txt
    with open("d.txt", "r") as f:
        ll = f.readlines()
        mPass = ll[2]# hashed password value (needs to be matched to)
        print(mPass)
        print("---")
        attempts = 3
        while attempts > 0:
            master_input =str(input("Please enter your Master Password: ")).encode()
            if bcrypt.checkpw(master_input, mPass.encode()):
                key = mPass[:16] # error: key is not defined
                am.Abyss()
                MainMenu()
            else:
                am.Abyss()
                print("Incorrect password! Try again.\n")
                attempts -= 1
            if attempts == 0:
                am.Abyss()
                End("Too many password attempts")


def MainMenu():
    """
    Main menu prompt that gives the user access to the programs main function...
        User's accounts data
        Change password for an existing account
        Remove an account
        Modify account
    :return:
    """
    Export() #
    Import()
    print("Main Menu".center(60, ' ') + "\n" + "-" * 60 + "\n")
    print("Welcome back, {}".format(mName).center(60, ' '))
    print("\n 1)  Find the password for an existing Website/App\n",
          "2)  Add new Website/App and new password for it\n",
          "3)  Change an existing password for an existing Website/App\n",
          "4)  Remove an existing App/Website\n",
          "5)  Account Options\n",
          "6)  Exit\n")

    #infinite while loop for user input
    while True:
        try:
            uChoice = int(input(" - "))
            if uChoice in range(1, 7):
                if uChoice == 1:
                    FindPassword()
                if uChoice == 2:
                    AccAdd()
                if uChoice == 3:
                    ModAcc()
                if uChoice == 4:
                    RemoveAcc()
                if uChoice == 5:
                    UserOptions()
                if uChoice == 6:
                    Export()
                    End()
            else:
                print("Please only enter numbers!")
        except ValueError:
            print("Please only enter numbers!")


def ReturnToMenu(msg="\nWould you like to return to the menu? (Y/N)"):
    """
    User prompt to return to main menu

    User input has to be either 'y' or 'n'

    :param msg:
        changes prompt

    """
    while True:
        print(msg)
        p = str(input(" - ")).lower()
        if 'y' in p:
            am.Abyss()
            MainMenu()
        if 'n' in p:
            return
        else:
            print("Please enter Y or N")
            continue


def FindPassword():
    """

    :return:
    returns password based off of selected website
    """
    global accWeb, accUser, accPass
    if len(accUser) == 0:
        print("No accounts!")
        MainMenu()
    while True:
        am.Abyss()
        print("".ljust(10) + len(accUser).str() + " Logins:")
        print("".ljust(10) + "Type 'm' to go back to the main menu")
        print("".ljust(10) + "Website:".ljust(22) + "Username:".ljust(25) + "Password:\n")
        for index in range(0, len(accWeb)):
            print("".ljust(10) + accWeb[index].ljust(22) + accUser[index].ljust(23) + "\t" + "*" * len(accPass[index]))
        uChoice = str(input("\nFor which website would you like your login information?")).lower()
        if uChoice == 'm':
            ReturnToMenu()
        if uChoice in accWeb:
            am.Abyss()
            print("".ljust(10) + "Website:".ljust(22) + "Username:".ljust(25) + "Password:\n")
            print("".ljust(10) + str(accWeb[accWeb.index(uChoice)]).ljust(22) + str(
                accUser[accWeb.index(uChoice)].ljust(25) + str(accPass[accWeb.index(uChoice)])))
            ReturnToMenu()
        else:
            continue

        # condition for a non-existant index
        if not uChoice in accUser:
            am.Abyss()
            uChoiceAdd = str(input(
                "\n" + uChoice + " does not seem to exist within our system. Would you like to add it?(Y/N)")).upper()
            if uChoiceAdd == 'Y':
                AccAdd(uChoice)


def AccAdd(site=""):
    """

    :param site:
        parameter to prevent the redudant repetition of website prompt
    :return:
    """
    global accWeb, accUser, accPass
    if site == "":
        nSite = str(input("Please enter the address for " + site + "\n - ")).encode()

    nUser = str(input("Please enter the username for " + site + "\n - ")).encode()
    nPass = str(input("Please enter the password for " + site + "\n - ")).encode()
    accWeb.append(site.lower())
    accUser.append(nUser)
    accPass.append(nPass)
    am.Abyss()
    Export()
    print("Account added")
    MainMenu()


def RemoveAcc():
    """
    Removes a selected account

    """
    global accWeb, accUser, accPass
    am.Abyss()
    print("Please input the number for the account you want to remove:")
    print("".ljust(10) + "Website:".ljust(22) + "\n")
    for i in range(0, len(accWeb)):
        print("".ljust(5), "{}".format(i + 1), accWeb[i].ljust(20))

    print("\n      {}). Cancel".format(len(accWeb) + 2))
    # infinite while loop to choose account for deletion
    while True:
        try:
            uChoice = int(input(" - "))
            if uChoice in range(1, len(accWeb) - 1):
                del accWeb[uChoice - 1] # deletes index from list
                del accUser[uChoice - 1]
                del accPass[uChoice - 1]
                am.Abyss()
                print("Account Removed")
                Export()
                MainMenu()

            if uChoice == (len(accWeb) + 1):
                am.Abyss()
                MainMenu()
            else:
                print("Please only enter numbers")
        except ValueError:
            print("Please only enter numbers")


def ModAcc():
    """
    Prompt for modification of user's accounts...
        Change web address of stored account
        Change Username of stored account
        Change Password of stored account

    """
    global accWeb, accUser, accPass
    am.Abyss()
    print(len(accUser), " Logins:")
    print("".ljust(10) + "Website:".ljust(22) + "Username:".ljust(25) + "Password:\n")
    for index in range(0, len(accWeb)):
        print("".ljust(10) + accWeb[index].ljust(22) + accUser[index].ljust(23) + "\t" + "*" * len(accPass[index]))
    print("\n      {}). Cancel".format(index + 2))

    # infinite while loop for user input
    while True:
        try:
            uChoiceAcc = int(input(" - "))
            if uChoiceAcc in range(1, len(accWeb) + 1):
                print(accWeb[uChoiceAcc] + "\n")
                print("Enter the number corresponding to desired feature:\n\n",
                      "1)Change web address\n",
                      "2)Change username\n",
                      "3)Change password\n",
                      "4)Main Menu")
                while True:
                    try:
                        uChoice = int(input(" - "))
                        if uChoice in range(1, 5):
                            break
                        else:
                            print("Please only enter numbers on the menu")
                    except ValueError:
                        print("Please only enter numbers")
                if uChoice == 1:
                    accWeb[uChoiceAcc] = str(input("Please enter the new web address")).lower()
                    am.Abyss()
                    Export()
                    MainMenu()
                if uChoice == 2:
                    accUser[uChoiceAcc] = str(input("Please enter the new username"))
                    am.Abyss()
                    Export()
                    MainMenu()
                if uChoice == 3:
                    accPass[uChoiceAcc] = str(input("Please enter the new password"))
                    am.Abyss()
                    Export()
                    MainMenu()
                if uChoice == 4:
                    MainMenu()

            if uChoiceAcc == (len(accWeb) + 1):
                am.Abyss()
                MainMenu()
            else:
                print("Please only enter numbers on the menu")

        except ValueError:
            print("Try Again! Please only enter numbers on the menu!")


def UserOptions():
    """
    Prompt for account options including...
        changing the master password
        changing the user name

    :return:
    """
    print("Account options for\nEnter the number of the desired function\n",
          "1)  Change Master Password\n",
          "2)  Change Display Name\n",
          "3)  Return to menu\n")
    while True:
        try:
            uChoice = int(input(" - "))
            if uChoice in range(1, 4):
                break
            else:
                print("Please only enter numebrs on the menu!")
        except ValueError:
            print("Please only enter numbers on the menu!")
    if uChoice == 1:
        am.Abyss()
        SetmPass()
        print("Your master password has been changed")
        UserOptions()
    if uChoice == 2:
        am.Abyss()
        SetmName()
        print("Your name has been changed")
        UserOptions()
    if uChoice == 3:
        am.Abyss()
        MainMenu()


def End(cause=""):

    """
    Method to end program
    :param cause:
        given cause for ending
    """
    global mPass
    print("Now Exiting, {}. Have a nice day!".format(cause))
    mPass = ''
    exit(0)


StartMenu()
