from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import win32gui
import win32process
import wmi
import time
import threading
import pythoncom
import argparse
import pprint
import textwrap


class Volumer(threading.Thread):

    def __init__(self, args):
        threading.Thread.__init__(self)
        self.registered = list()
        self.previous_volumes = dict()
        self.__handle_args(args)

    def __handle_args(self, args):
        """
        Handles arguments of programs and appends it to registered processes
        :param args: argparse namespace
        """
        if isinstance(args, argparse.Namespace):
            # Handle file
            try:
                file = open(args.file, 'r')
                self.registered.extend(file.readlines())
                file.close()
            except:
                pass
            # Handle list
            try:
                self.registered.extend(args.list)
            except:
                pass
            # Make registered unique
            self.registered = list(set(self.registered))
            self.registered.sort()

    def set_process_volume(self, process_name, volume_level):
        """
        Sets volume of process found by process_name to volume_level
        :param process_name: name of process
        :param volume_level: value to set valume to (0.0 - 1.0)
        """
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name().lower() == process_name.lower():
                self.previous_volumes[process_name] = volume.GetMasterVolume()
                volume.SetMasterVolume(volume_level, None)

    def get_process_volume(self, process_name):
        """
        Get current process volume by name
        :param process_name: name of process
        :return: volume of process or None
        """
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name().lower() == process_name.lower():
                return volume.GetMasterVolume()
        return None

    def set_process_volume_zero(self, process_name):
        """
        Sets process volume to 0.0
        :param process_name: name of process
        """
        self.set_process_volume(process_name, 0.0)

    def set_process_volume_max(self, process_name):
        """
        Sets process volume to 1.0
        :param process_name: name of process
        """
        self.set_process_volume(process_name, 1.0)

    def restore_process_volume(self, process_name):
        """
        Restore previous saved volume for process
        :param process_name: process_name
        """
        if process_name in self.previous_volumes.keys():
            prev = self.previous_volumes[process_name]
            if isinstance(prev, float) or isinstance(prev, int):
                self.set_process_volume(process_name, prev)
                del self.previous_volumes[process_name]

    def is_focused(self, process_name):
        """
        Checks if process main window is in foreground
        :param process_name:
        :return: True or False
        """
        focused = self.get_focused()
        if process_name is None or focused is None:
            return False
        if isinstance(process_name, str) and focused.lower() == process_name.lower():
            return True
        return False

    def get_focused(self):
        """
        Returns name of process that has its main window currently in foreground
        :return: name of process or None
        """
        hwd = win32gui.GetForegroundWindow()
        an = self.__get_app_name(hwd)
        return an

    def __get_app_name(self, hwnd):
        """
        Translates Windows handler to process name
        :param hwnd: handle of window
        :return:
        """
        c = wmi.WMI()
        exe = None
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
                exe = p.Name
                break
        except:
            return None
        else:
            return exe

    def run(self):
        """
        Main thread of volumer
        """
        # Neccessary magic
        pythoncom.CoInitialize()

        if len(self.registered) < 1:
            print("No processes found, volumer not started")
            return

        print("Volumer started!")
        output = "Registered: "
        output = output + ", ".join(self.registered)
        print(*textwrap.wrap(output, width=85), sep='\n')
        print()

        while True:
            for listed in self.registered:
                start_sound_level = self.get_process_volume(listed)

                if not self.is_focused(listed):
                    if self.get_process_volume(listed) != 0:
                        self.set_process_volume(listed, 0)
                else:
                    self.restore_process_volume(listed)

                end_sound_level = self.get_process_volume(listed)

                if start_sound_level != end_sound_level:
                    print("Sound for {} has changed from {} to {}".format(listed, start_sound_level, end_sound_level))

            time.sleep(1)

        print()
        print("Volumer disabled!")


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help="file with list of processes")
    parser.add_argument('-l','--list', nargs='+', help='list of processes')
    return parser.parse_args()


def main():
    """
    Main function
    """
    args = setup_parser()

    volumer = Volumer(args)
    volumer.start()
    volumer.join()

    print("---")


if __name__ == "__main__":
    main()
