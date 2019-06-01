import psutil
import os
import sys
from pathlib import Path
import shutil

CONFIG_DIRECTORY = os.getenv('APPDATA') + "\\Sognus\\process-killer\\"
CONFIG_FILE = "kill_list.txt"  
CONFIG_PATH = CONFIG_DIRECTORY + CONFIG_FILE

def process_args():
	args = sys.argv
	
	# Clean all folders
	if "clean" in args:
		folder = Path(CONFIG_DIRECTORY)
		parent = folder.parent
	
		# If killer folder exist it deletes it
		if os.path.isdir(folder):
			print(f"Deleting {str(folder)}")
			shutil.rmtree(folder, ignore_errors=True)
		
		# If Sognus folder exist and its EMPTY it will be deleted
		parent_content = os.listdir(parent)
		if os.path.isdir(parent) and len(parent_content) < 1:
			print(f"Deleting {str(parent)}")
			shutil.rmtree(parent, ignore_errors=True)
		
		sys.exit(0)
	

def main():
	# Pre-Init
	kill_list = list()
	
	# Create config folder if it does not exist
	os.makedirs(CONFIG_DIRECTORY, exist_ok=True)
	# Create file if it does not exist
	if not os.path.isfile(CONFIG_PATH):
		print("Config file does not exist, creating one in "+CONFIG_PATH)
		with open(CONFIG_PATH, "w+") as config_file:
			config_file.write("# Insert process name here\n")
			config_file.write("# Every line means one process name\n")
			config_file.write("# Use '#' character for comments\n")
	else:
		with open(CONFIG_PATH, 'r') as reader:
			content = reader.readlines()
			for line in content:
				if not line.startswith("#"):
					print(f"Adding {line} to kill list.")
					kill_list.append(line)
	
	
	# Detect config file in current folder
	if os.path.isfile(CONFIG_FILE):
		print("Configuration file was found in current folder, including to killer list")
		with open(CONFIG_PATH, 'r') as reader:
			content = reader.readlines()
			for line in content:
				if not line.startswith("#"):
					print(f"Adding {line} to kill list.")
					kill_list.append(line)
	else:
		print("Configuration file not found in current folder. You can create one creating kill_list.txt")
	
	# Check if we have processes
	if len(kill_list) < 1:
		print("Kill list is empty, terminating!")
		return
		
	
	# Kill all processes
	for process in psutil.process_iter():
		try:
			if process.name() in kill_list:
				print(f"Killing {process.name()}")
				process.kill()
		except:
			print("Could not access process")
	

if __name__ == "__main__":
	process_args()
	main()