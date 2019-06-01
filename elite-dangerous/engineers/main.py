import argparse
import json
import os
import sys
import cmd

from json.decoder import JSONDecodeError


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help="Json file to parse", required=True, dest="data_filename", metavar="<json file path>")
    return parser


def print_error(message):
    print(message, file=sys.stderr)

class Console(cmd.Cmd):
    intro = 'Welcome Elite Dangerous engineer prompt. Type help or ? to list commands.'
    prompt = '> '

    def __init__(self, data_json):
        super().__init__()
        self.data = data_json
        self.selected = None

    # -------------------------------
    # Program logic
    # -------------------------------
    def is_selected(self):
        # Auto fix
        if self.selected is None or self.selected < 0 or self.selected > len(self.data):
            self.selected = None
        # If selected is none, nothing is selected
        if self.selected is None:
            return False
        return True



    # -------------------------------
    # Console logic
    # -------------------------------
    def do_menu(self, args):
        print("Found {} ship builds:".format(len(self.data)))
        for i in range(len(self.data)):
            print("[{}] {} ({})".format(i, self.data[i]["ship"], self.data[i]["name"]))

    def do_select(self, args):
        args = args.split(' ')
        if len(args) < 1:
            print("You need to specify which build you want to select!")
            return
        if not args[0].isdigit():
            print("Argument must be a number. Type menu to see IDs!")
            return
        pre_select = int(args[0])
        if pre_select < 0 or pre_select > len(self.data):
            print("Invalid selection ID. Type \"menu\" to see IDs!")
            return
        self.selected = int(pre_select)
        print("{} ({}) selected!".format(self.data[self.selected]["ship"], self.data[self.selected]["name"]))

    def do_selected(self, args):
        if not self.is_selected():
            print("No build selected!")
        else:
            print("{} ({}) selected!".format(self.data[self.selected]["ship"], self.data[self.selected]["name"]))

    def do_components(self, args):
        # Use first argument as build selector
        if len(args) > 0:
            self.do_select(args)

        if not self.is_selected():
            print("No build selected. Please select one with \"select <ID>.\"")
            return

        # Print components now
        for type in self.data[self.selected]["components"]:
            print("    "+type)
            item = self.data[self.selected]["components"][type]

            banned = ("hardpoints", "utility", "internal")
            if type in banned:
                continue

            for i in item:
                if isinstance(item[i], str):
                    print("        {}".format(str(item[i])))
                else:
                    print("        {}".format(str(item[i])))
                print()
                print()




if __name__ == '__main__':
    # Check for arguments included in argparse
    parser = setup_parser()
    args = parser.parse_args()

    # Check if file exist
    if not os.path.isfile(args.data_filename):
        print_error("ERROR 1: File does not exist!")
        parser.print_usage()
        exit(1)

    # Check if file can be accessed
    if not os.access(args.data_filename, os.R_OK):
        print_error("ERROR 2: File exist but cannot be read! (permissions?)")
        parser.print_usage()
        exit(2)

    # Open file for
    with open(args.data_filename, 'r') as data_file:
        try:
            data_json = json.load(data_file)
        except JSONDecodeError:
            print_error("ERROR 3: File content is not valid json!")
            parser.print_usage()
            exit(3)

        print()

        Console(data_json).cmdloop()


