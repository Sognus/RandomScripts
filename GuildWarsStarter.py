import os
from os import path
import yaml
import psutil
import subprocess
import time
import logging
import sys
import ctypes
import signal

# STATIC
CONFIG = path.expandvars(r'%APPDATA%\Sognus\GwStarter')


# CLASS
class Starter:

    def __init__(self):
        self.logger = None
        self.logging()
        self.started_programs = dict()
        self.logger.info("Program started")
        self.cfg = None
        self.config()
        self.start()

    def logging(self):
        self.logger = logging.getLogger("GuildWarsStarter")
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(CONFIG + r"\GuildWarsStarter.log")
        log_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-3s %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        file_handler.setFormatter(log_formatter)
        std_handler = logging.StreamHandler(sys.stdout)
        std_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(std_handler)

    def config(self):
        if not os.path.exists(CONFIG):
            self.logger.info("Configuration folder does not exist, attempting to create it.")
            os.makedirs(CONFIG)

        file_path = CONFIG + r"\configuration.yaml"
        cfg = dict()

        if not path.isfile(file_path):
            ctypes.windll.user32.MessageBoxW(None, u"Configuration is missing!", u"Error", 0x10)
            self.logger.info("Configuration file does not exist, attempting to create it.")

            cfg["umod"] = dict()
            cfg["umod"]["enabled"] = 1
            cfg["umod"]["location"] = "<insert umod exe location here>"
            cfg["umod"]["delay"] = 0

            cfg["gw"] = dict()
            cfg["gw"]["enabled"] = 1
            cfg["gw"]["location"] = "<insert gw.exe location here>"
            cfg["gw"]["delay"] = 10

            cfg["gwtb"] = dict()
            cfg["gwtb"]["enabled"] = 1
            cfg["gwtb"]["location"] = "<insert gwtb exe location here>"
            cfg["gwtb"]["delay"] = 0

            with open(file_path, 'w') as yaml_file:
                yaml.dump(cfg, yaml_file, default_flow_style=False)

            subprocess.Popen('explorer "{}"'.format(CONFIG))
        else:
            self.logger.info("Configuration file found, reading...")

            with open(file_path, 'r') as yaml_file:
                cfg = yaml.load(yaml_file)

            # Check for valid locations
            failed_list = list()

            self.logger.info("Checking configuration file...")

            for main_key in cfg:
                self.logger.info("Checking key: " + main_key)

                for key in cfg[main_key]:
                    self.logger.info("Checking subkey: " + key)
                    # Skip non-file configuration keys
                    if key != "location":
                        continue
                    # Check if file configuration key is valid file
                    if not os.path.isfile(cfg[main_key][key]):
                        if cfg[main_key]["enabled"] == 1:
                            self.logger.info("{}.{}: file not found".format(main_key, key))
                            failed_list.append("{}.{} is not valid file".format(main_key, key))

                self.logger.info("***")

            if len(failed_list) > 0:
                self.logger.info("Configuration validation unsucessfull!")
                string = ""
                for err in failed_list:
                    string = string + err + "\n"
                ctypes.windll.user32.MessageBoxW(None, u"Configuration errors detected!\n\n" + string, u"Error", 0x10)
                subprocess.Popen('explorer "{}"'.format(CONFIG))
            else:
                self.logger.info("Configuration validation sucessfull!")
                self.cfg = cfg

    def start(self):
        try:
            if self.cfg is None:
                self.logger.error("Internal error - Starter.cfg cannot be None!")
                return

            programs = ["umod", "gw", "gwtb"]
            for program in programs:
                if self.cfg[program]["enabled"] == 1:
                    self.logger.info("Trying to run " + program)
                    process = subprocess.Popen('"{}"'.format(self.cfg[program]["location"]),
                                               cwd=os.path.dirname(self.cfg[program]["location"]))
                    self.started_programs[program] = process.pid
                    self.logger.info("Process {} pid is {}".format(program, process.pid))
                    self.logger.info("Initiated {} second delay".format(self.cfg[program]["delay"]))
                    time.sleep(self.cfg[program]["delay"])

            self.logger.info("*")
            self.logger.info("Waiting for GuildWars to be terminated...")

            # Initiate wait-to-end
            while True:
                if psutil.pid_exists(self.started_programs["gw"]):
                    time.sleep(1)
                    continue
                # PID DEAD - KILL OTHERS
                self.logger.info("GuildWars terminated, killing other PIDs")
                for key, value in self.started_programs.items():
                    if psutil.pid_exists(int(value)):
                        self.logger.info(
                            "Killing process {program} with pid {pid}".format(program=str(key), pid=int(value)))
                        os.kill(int(value), signal.SIGTERM)
                break

            self.logger.info("Program ended")
            self.logger.info("******")
            self.logger.info("******")
        except Exception as e:
            import sys
            self.logger.error(sys.exc_info()[0])
            import traceback
            self.logger.error(traceback.format_exc())
            ctypes.windll.user32.MessageBoxW(None,
                                             u"An exception occured, please contact author: \n\nhttps://github.com/Sognus",
                                             u"Error", 0x10)


# Admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# MAIN
def main():
    starter = Starter()


# ENTRY POINT
if __name__ == "__main__":
    if is_admin():
        # Started as administrator - its fine
        main()
    else:
        # Started as user - rerun as administrator
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
