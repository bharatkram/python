import os
import os.path
# to get the name of file without extension.
from pathlib import Path


singleCommandsList = ("cls", "help", "dir", "exit")
dependantCommandsList = ("cat", "sort")


# function to run the single word commands.
def singleCommands(command):
    global singleCommandsList
    global dependantCommandsList
    # print(command)

    # tuple to store the details of all single word commands.
    singlecommands = ("\033[1mcls\033[0m - clears the screen", "\033[1mhelp\033[0m - shows all the commands",
                      "\033[1mdir\033[0m - shows all the files in the present directory", "\033[1mexit\033[0m - exit the program.")
    # tuple to store the details of all dependent commands.
    dependantcommands = ("\033[1mcat\033[0m - reads contents of the file",
                         "\033[1msort\033[0m - prints sorted order of the contents of folder")

    if len(singleCommandsList) != len(singlecommands):
        print("Single commands details not covered.")

    if len(dependantCommandsList) != len(dependantcommands):
        print("Commands details not covered.")

    if command == "cls":
        os.system("cls")
    elif command == "help":
        print(*sorted(singlecommands + dependantcommands), "", sep="\n")
    elif command == "dir":
        print("", *os.listdir(), "", sep="\n")


# function to sort the inputs as they are inserted.
def insertionSort(inpList, inp):
    inpList.append(inp)
    if len(inpList) == 1:
        return inpList
    pos = len(inpList) - 1
    while pos != 0:
        if inpList[pos] < inpList[pos - 1]:
            inpList[pos], inpList[pos - 1] = inpList[pos - 1], inpList[pos]
            pos -= 1
            continue
        break
    return inpList


# function to take inputs from user that are to be sorted.
def takeInputs():
    inpList = []
    while True:
        try:
            inp = input()
            # if input is a empty.
            if inp.strip() == "":
                continue
            inpList = insertionSort(inpList, inp)
        # break the loop if the user inputs ctrl+c.
        except KeyboardInterrupt:
            print("", *inpList, sep="\n")
            return


# function to sort the contents in file and output them to file or panel as per users input.
def sortContents(fileName, reverse, output):
    # print(os.getcwd())
    cwd = os.getcwd()

    # to read the contents of a file and split by end of line.
    file = open(cwd + "/" + fileName, "r")
    contents = file.read().splitlines()
    file.close()

    # sorting the contents as per the requirement.
    contents.sort(reverse=reverse)

    # check where the output is to be given.
    if not output:
        print(*contents, sep="\n")
    else:
        if os.path.isfile(output):
            inp = input("Do you want to rewrite the file?(y/n)")
            if inp not in ["y", "Y"]:
                return

        # to write to the specified file.
        file = open(cwd + "/" + output, "w")
        file.write("\n".join(contents))
        file.close()


# function to execute each flag and parse the command.
def sortWithDependants(command, dependants):
    # variable to know if the sorting is to be done in the reverse order.
    reverse = False
    # variable to know if the sorted order is to be saved in a file or output to screen.
    output = False
    # variable to get the filename whose contents are to be sorted.
    fromFile = ""

    # tuple to store the available single letter flags.
    singleLetterFlags = ("-r", "-o")
    # tuple to store the available double dash flags.
    doubleDashFlags = ("--reverse", "--output")
    while dependants != "":
        # line to separate each word in the command.
        flag, _, dependants = dependants.partition(" ")

        # to know if the word in the command is a flag.
        if flag[0] == "-":
            # to know if the double dash function is recognised.
            if flag[1] == "-" and flag.split("=")[0] in doubleDashFlags:
                pass
            # to know if the single letter function if recognised.
            elif flag[:2] in singleLetterFlags:
                pass
            # if the flag is not recognised.
            else:
                print(f"{flag} not recognised.")
                return

        if flag == "-r" or flag == "--reverse":
            reverse = True
        elif flag[:2] == "-o":
            if len(flag) != 2:
                output = flag[2:]
            else:
                output, _, dependants = dependants.partition(" ")
        elif flag[:8] == "--output":
            flag = flag.split("=")
            if len(flag) == 1:
                output, _, dependants = dependants.partition(" ")
            else:
                output = flag[1]
        else:
            if fromFile == "":
                fromFile = flag
            else:
                print("Given two file names. Needed only one.")
                return

    # to know the file name is given from where the input is to be read.
    if fromFile == "":
        print("Required a filename to read from.")
        return
    # to know if the file exists.
    if not os.path.isfile(fromFile):
        print("File not found.")
        return
    # to perform the task given.
    sortContents(fromFile, reverse, output)


# to segregate if the command depends on a file or user inputs the values.
def sortCommand(command, dependants):
    if not dependants:
        takeInputs()
        return
    sortWithDependants(command, dependants)


# to perform the read operation.
def catCommand(command, dependants):
    print("cat called")
    return


# to call the function according to the command.
def dependantCommands(command, dependants):
    commands = {"sort": sortCommand, "cat": catCommand}
    commands[command](command, dependants)
    return


if __name__ == "__main__":
    while True:
        inp = input(f"$$ {Path(__file__).stem} >").strip()

        # if input is a empty.
        if inp.strip() == "":
            continue

        # if exit is the command.
        if inp == "exit":
            break

        # separate the command from the input string.
        command, _, rest = inp.partition(" ")
        # print(f"{command}\n{rest}")

        # check if the command is recognised.
        if command not in singleCommandsList and command not in dependantCommandsList:
            print(f"No such command as {command}\n")
            continue

        # checking if the command is present in the list.
        if command in singleCommandsList:
            # checking if any parameters are passed which aren't necessary.
            if not rest:
                singleCommands(command)
                continue
            print(
                f"\n{command} takes no arguments such as {rest.split()[0]}\ntype help to know all commands.\n")
            continue

        dependantCommands(command, rest)
