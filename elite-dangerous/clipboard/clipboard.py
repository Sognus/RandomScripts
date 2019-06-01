import tkinter
import threading
import csv
import argparse
import pyperclip
import os
import win32gui
import sys
from time import sleep
from system_hotkey import SystemHotkey


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', help="csv file to parse", required=True, dest="data_filename",
                        metavar="<csv file path>")
    parser.add_argument('-y', '--clipboard-yes', help='clipboard change enabled', dest="clipboard",
                        action='store_true')
    parser.add_argument('-n', '--clipboard-no', help='clipboard change disabled', dest="clipboard",
                        action='store_false')
    return parser


def parse_csv(csv_filename):
    rows = list()
    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in list(csv_reader)[1:]:
            rows.append(row[0])
    return rows


class App(threading.Thread):

    @property
    def current_data(self):
        return self.data[self.current][1:-1]

    @property
    def previous_data(self):
        if self.current - 1 >= 0:
            return self.data[self.current - 1][1:-1]
        return None

    @property
    def next_data(self):
        if self.current + 1 <= len(self.data) - 1:
            return self.data[self.current + 1][1:-1]
        return None

    '''
    Terrible cheat
    '''

    def update_text(self):
        self.label_progress["text"] = f'({self.current + 1}/{len(self.data)})'

        length_current = len(self.label_current["text"])
        length_progress = len(self.label_progress["text"])

        # Top text is longer than botton text
        if length_current > length_progress:
            needed_non_divis = abs(length_current - length_progress)
            needed = abs(length_current - length_progress) / 2
            # divisible by 2
            if (needed_non_divis % 2) == 0:
                self.label_progress["text"] = " " * int(needed) + self.label_progress["text"] + " " * int(needed)
            else:
                # Top text is odd, need to append one more
                if length_current % 2 != 0:
                    self.label_current["text"] = self.label_current["text"] + " "
                    length_current = length_current + 1
                elif length_progress % 2 != 0:
                    self.label_progress["text"] = self.label_progress["text"] + " "
                    length_progress = length_progress + 1
                # Fixed needed
                needed = abs(length_current - length_progress) / 2
                self.label_progress["text"] = " " * int(needed) + self.label_progress["text"] + " " * int(needed)
        else:
            print("ERROR - NOT IMPLEMENTED ", file=sys.stderr)
            pass
            # TODO: top text is shorter than bottom text
        # Update text size
        self.label_progress.master.geometry(
            f"+{int((self.screen_width / 2) - (self.label_progress.winfo_width()/2))}+300")
        self.label_current.master.geometry(
            f"+{int((self.screen_width / 2) - (self.label_current.winfo_width()/2))}+200")

    def __init__(self, data, clipboard=None):
        threading.Thread.__init__(self)

        # List of strings
        self.data = data
        # Pointer to current data
        self.current = 0
        # Is GUI visible
        self.visible = True
        # Makes PyCharm happy
        self.hk = None
        # Kill flag
        self.kill = False

        # Get screen size
        root = tkinter.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Create current
        self.label_current = tkinter.Label(text=f'{self.current_data}', font=('Consolas', '30'), fg='red', bg='black')
        self.label_current.master.overrideredirect(True)
        self.label_current.master.lift()
        self.label_current.master.wm_attributes("-topmost", True)
        self.label_current.master.wm_attributes("-disabled", True)
        self.label_current.master.wm_attributes("-transparentcolor", "black")
        self.label_current.pack()

        # Create pointer
        self.label_progress = tkinter.Label(text=f'({self.current + 1}/{len(self.data)})', font=('Consolas', '30'),
                                            fg='red', bg='black')
        self.label_progress.master.overrideredirect(True)
        self.label_progress.master.lift()
        self.label_progress.master.wm_attributes("-topmost", True)
        self.label_progress.master.wm_attributes("-disabled", True)
        self.label_progress.master.wm_attributes("-transparentcolor", "black")
        self.label_progress.pack()

        # Clipboard
        self.modify_clipboard = False if clipboard is None else not clipboard
        self.toggle_clipboard()

        # update text
        self.update_text()
        self.next()
        self.previous()

        # start hotkeys
        self.start()

        # start label loop
        self.label_current.master.mainloop()

    def previous(self):
        # print("DEBUG: PREVIOUS")
        if self.previous_data is not None:
            self.current = self.current - 1
            self.label_current["text"] = self.current_data
            self.update_text()
            self.label_current.update()
            if self.modify_clipboard:
                pyperclip.copy(self.current_data)

    def next(self):
        # print("DEBUG: NEXT")
        if self.next_data is not None:
            self.current = self.current + 1
            self.label_current["text"] = self.current_data
            self.update_text()
            self.label_current.update()
            if self.modify_clipboard:
                pyperclip.copy(self.current_data)

    def toggle_clipboard(self):
        self.modify_clipboard = not self.modify_clipboard
        color = 'white' if self.modify_clipboard else "red"
        self.label_current["fg"] = color
        self.label_progress["fg"] = color
        self.label_current.update()
        self.label_progress.update()
        print(f"Automatic clipboard is {'disabled' if self.modify_clipboard is False else 'enabled'}")

    def toggle_visible(self):
        self.visible = not self.visible

    def app_exit(self):
        print("Terminating application")
        self.hk.unregister(('control', 'kp_4'))
        self.hk.unregister(('control', 'kp_6'))
        self.hk.unregister(('control', 'kp_5'))
        self.hk.unregister(('control', 'kp_0'))
        self.hk.unregister(('control', 'kp_8'))
        self.kill = True
        self.label_progress.master.quit()

    def run(self):
        self.hk = SystemHotkey()
        self.hk.register(('control', 'kp_4'), callback=lambda x: self.previous())
        self.hk.register(('control', 'kp_6'), callback=lambda x: self.next())
        self.hk.register(('control', 'kp_5'), callback=lambda x: self.toggle_clipboard())
        self.hk.register(('control', 'kp_0'), callback=lambda x: self.app_exit())
        self.hk.register(('control', 'kp_8'), callback=lambda x: self.toggle_visible())

        while True:
            active_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())

            if active_window_name.lower() == "Elite - Dangerous (CLIENT)".lower() and self.visible:
                # show
                self.label_progress.master.deiconify()
            else:
                pass
                # hide
                self.label_current.master.withdraw()

            # Check for kill flag
            if self.kill:
                break

            # Sleep
            sleep(1)


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()

    # Check if file exist
    if not os.path.isfile(args.data_filename):
        print("ERROR 1: File does not exist!")
        parser.print_usage()
        exit(1)

    # Check if file can be accessed
    if not os.access(args.data_filename, os.R_OK):
        print("ERROR 2: File exist but cannot be read! (permissions?)")
        parser.print_usage()
        exit(2)

    data = parse_csv(args.data_filename)
    app = App(data, clipboard=args.clipboard)
