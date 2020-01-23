from sys import exit  # imports exit method from system module
import sys,re,os # module import
import io
import am #seperate methods am.py
import bcrypt
import e #AES encryption for user data

#Main method that is basically the framework
def StartMenu():
    global accWeb,accUser,accPass # global variables for data
    am.Abyss()
    sys.tracebacklimit=0
    print("Welcome to Panty".center(35, ' ')+"\n")
    am.Abyss()

    accWeb=[]
    accUser=[]
    accPass=[]

    if (am.CheckFileExists("d.txt") != True):
        SetmName()
        SetmPass()
        MainMenu()


    print("Enter the number coresponding to desired feature:\n\n",
        "1)Log-In\n",
        "2)Exit\n")
    while True:
        try:
            uChoice=int(input())
            if uChoice in range(1,3):
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
    global mName
    while True:
        mName=input("Please enter a name using only letters\n - ")
        if not re.match("[a-z,A-Z]*$", mName):
            print("Only letters please")
            continue
        else:
            am.Abyss()
            break

def SetmPass():
    global mPass
    while True:
        flag=0
        print("Your master password must:\n\t- Contatin 8-16 characters\n\t- Contain at least 1 Lowercase letter\n\t- Contain at least 1 Uppercase letter\n\t- Contain at least 1 number\n\t- Contain at least 1 special character(!@#$)\n")
        mPass=str(input("Input master password: \n - ")).encode("utf-8")

        if len(mPass) < 8:
            print("Must be at least 8 characters\n")
            flag=-1

        if len(mPass) > 16:
            print("Must be shorter than 16 characters\n")
            flag=-1

        if ' ' in mPass:
            print("Cannot contain spaces")
            flag=-1

        if not re.search("[0-9]",mPass):
            print("Must contain a number")
            flag=-1

        if not re.search("[A-Z]",mPass):
            print("Must contain at least 1 uppercase letter")
            flag=-1

        if not re.search("[!@#$]",mPass):
            print("Must contain at least 1 special character")
            flag=-1

        if not re.search("[a-z]",mPass):
            print("Must contain at least 1 lowercase letter")
            flag=-1

        if flag == 0:
            break

        else:
            print("Please make sure your master password follows our requirements")

def HashPass(p):
    if p == "":
        return ''
    else:
        salt = bcrypt.gensalt(16)
        return bcrypt.hashpw(p.encode("utf-8"), salt)

#Method to export encrypted user accounts
def Export():
    global mName, mPass, accWeb, accUser, accPass,f
    with open("d.txt","w+") as f:  #Sets a file name creates new file if it does not exist
      f.write("{}\n{}\n".format(mName,HashPass(mPass)))
      for i in range(len(accWeb)):                       
        f.write("{}:{}:{}\n".format(e.encrypt(accWeb[i],key),e.encrypt(accUser[i],key),e.encrypt(accPass[i],key)))

def Import():
    global accWeb,accUser,accPass,mPass,mName,f
    with open("d.txt", "r+") as f:
        lineList = f.readlines()
        mName=lineList[0]
        mPass=lineList[1]
        if lineList[2] == '':
            return
        
        for i in range(2,len(lineList)):
            t=lineList[i].split(":")
            accWeb.append(str(decypt(t[0])),key)
            accUser.append(str(decypt(t[1])),key)
            accPass.append(str(decypt(t[2])),key)

def LogIn():
    global f, mName, mPass, inputPass, key
    with open('d.txt','r+') as f:
        lineList = f.readlines()
        attempts=3
        while attempts > 0:
            mPass=str(input("Please enter your Master Password: ")).encode("utf-8")
            if bcrypt.checkpw(mPass, lineList[1].encode("utf-8")):
                key=mPass[:16].encode("utf-8")##
                am.Abyss()
                mainMenu()
            else:
                am.Abyss()
                print("Incorrect password! Try again.\n")
                attemps-=1
            if attempts==0:
                am.Abyss()
                End("Too many password attemts")


def MainMenu():
    Export()
    Import()
    print("Main Menu".center(60,' ')+"\n"+"-"*60+"\n")
    print("Welcome back, {}\!".format(mName))
    print("\n 1)  Find the password for an existing Website/App\n",
          "2)  Add new Website/App and new password for it\n",
          "3)  Change an existing password for an existing Website/App\n",
          "4)  Remove an existing App/Website\n",
          "5)  Account Options\n",
          "6)  Exit\n")
    while True:
        try:
            uChoice=int(input(" - "))
            if uChoice in range(1,7):
                break
            else:
                print("Please only enter numbers!")
        except ValueError:
            print("Please only enter numbers!")
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
        export()
        End()

def ReturnToMenu(msg="\nWould you like to return to the menu? (Y/N)"):
    while True:
        print(msg)
        Polar=str(input(" - ")).lower()
        if 'y' in Polar:
            am.Abyss()
            MainMenu()
        if 'n' in Polar:
            return
        else:
            print("Please enter Y or N")
            continue

def FindPassword():
    global accWeb,accUser,accPass
    if len(accUser) == 0:
        print("No accounts!")
        return
    while True:
        am.Abyss()
        print("".ljust(10)+len(accUser)," Logins:")
        print("".ljust(10) + "Type 'm' to go back to the main menu")
        print("".ljust(10)+"Website:".ljust(22)+"Username:".ljust(25)+"Password:\n")
        for index in range(0,len(accWeb)):
            print("".ljust(10)+accWeb[index].ljust(22)+accUser[index].ljust(23)+"\t"+"*"*len(accPass[index]))
        uChoice=str(input("\nFor which website would you like your login information?")).lower()
        if uChoice is 'm':
            ReturnToMenu()
        if uChoice in accWeb:
            am.Abyss()
            print("".ljust(10)+"Website:".ljust(22)+"Username:".ljust(25)+"Password:\n")
            print("".ljust(10)+str(accWeb[accWeb.index(uChoice)]).ljust(22)+str(accUser[accWeb.index(uChoice)].ljust(25)+str(accPass[accWeb.index(uChoice)])))
            ReturnToMenu()
        else:
            continue

        if not uChoice in accUser:
            am.Abyss()
            uChoiceAdd=str(input("\n"+uChoice,"does not seem to exist within our system. Would you like to add it?(Y/N)")).upper()
            if uChoiceAdd == 'Y':
                AccAdd(uChoice)

def AccAdd(site=""):
    global accWeb,accUser,accPass
    if site=="":
        nSite=str(input("Please enter the address for "+site+"\n - ")).encode()

    nUser=str(input("Please enter the username for "+site+"\n - ")).encode()
    nPass=str(input("Please enter the password for "+site+"\n - ")).encode()
    accWeb.append(site).lower()
    accUser.append(nUser)
    accPass.append(nPass)
    am.Abyss()
    Export()
    print("Account added")
    MainMenu()

def RemoveAcc():
    global accWeb,accUser,accPass
    am.Abyss()
    print("Please input the number for the account you want to remove:")
    print("".ljust(10)+"Website:".ljust(22)+"\n")
    for i in range(0,len(accWeb)):
        print("".ljust(5),"{}".format(i+1),userApps[i].ljust(20))

    print("\n      {}). Cancel".format(i+2))
    while True:
        try:
            uChoice=int(input(" - "))
            if uChoice in range(1,len(accWeb)-1):
                del accWeb[uChoice-1]
                del accUser[uChoice-1]
                del accPass[uChoice-1]
                am.Abyss()
                print("Account Removed")
                Export()
                MainMenu()

            if uChoice == (len(accWeb)+1):
                am.Abyss()
                MainMenu()
            else:
                print("Please only enter numbers")
        except ValueError:
            print("Please only enter numbers")

def ModAcc():
    global accWeb,accUser,accPass
    am.Abyss()
    print(len(accUser)," Logins:")
    print("".ljust(10)+"Website:".ljust(22)+"Username:".ljust(25)+"Password:\n")
    for index in range(0,len(accWeb)):
        print("".ljust(10)+accWeb[index].ljust(22)+accUser[index].ljust(23)+"\t"+"*"*len(accPass[index]))
    print("\n      {}). Cancel".format(i+2))
    while True:
        try:
            uChoiceAcc=int(input(" - "))
            if uChoiceAcc in range (1,len(accWeb)+1):
                print(accWeb[uChoice]+"\n")
                print("Enter the number coresponding to desired feature:\n\n",
                "1)Change address\n",
                "2)Change username\n",
                "3)Change password\n",
                "4)Main Menu")
                while True:
                    try:
                        uChoice=int(input(" - "))
                        if uChoice in range(1,5):
                            break
                        else:
                            print("Please only enter numbers on the menu")
                    except ValueError:
                        print("Please only enter numbers")
                if uChoice == 1:
                    accWeb[uChoiceAcc]=str(input("Please enter the new web address")).lower()
                    am.Abyss()
                    Export()
                    MainMenu()
                if uChoice == 2:
                    accUser[uChoiceAcc]=str(input("Please enter the new username"))
                    am.Abyss()
                    Export()
                    MainMenu()
                if uChoice == 3:
                    accPass[uChoiceacc]=str(input("Please enter the new password"))
                    am.Abyss()
                    Export()
                    MainMenu()
                if uChoice == 4:
                    MainMenu()

            if uChoice  == (len(accWeb)+1):
                am.Abyss()
                MainMenu()
            else:
                print("Please only enter numbers on the menu")

        except ValueError:
             print("Try Again! Please only enter numbers on the menu!")

def UserOptions():
    print("Account options for\nEnter the number of the desired function\n",
    "1)  Change Master Password\n",
    "2)  Change Display Name\n",
    "3)  Return to menu\n")
    while True:
        try:
            uChoice=int(input(" - "))
            if uChoice in range(1,4):
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

def End(cause):
    global mPass
    print("Now Exiting, {}. Have a nice day!".format(cause))
    mPass=''
    exit(0)




StartMenu()
