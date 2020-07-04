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
        print("", *sorted(singlecommands + dependantcommands), "", sep="\n")
    elif command == "dir":
        print("", *os.listdir(), "", sep="\n")


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


def takeInputs():
    inpList = []
    while True:
        try:
            inp = input()
            # if input is a empty.
            if inp.strip() == "":
                continue
            inpList = insertionSort(inpList, inp)
        except KeyboardInterrupt:
            print("", *inpList, sep="\n")
            return


def sortCommand(command, dependants):
    if not dependants:
        takeInputs()
        return

    print("sort called")
    return


def catCommand(command, dependants):
    print("cat called")
    return


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
