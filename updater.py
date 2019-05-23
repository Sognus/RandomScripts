import requests
import os
import glob

# Constants
PAPER_API_URL = "https://papermc.io/api/v1/paper"
PAPER_MC_VERSION = "1.13.2"


class Updater:

    def __init__(self):
        # Latest minecraft version (IE. 1.13.2)
        self.mc_version_latest = None
        # Current used minecraft version
        self.mc_version = None
        pass

    # Requests for latest minecraft version that PaperMC supports
    # saves it to mc_version_latest and returns
    #
    # update_used_version:
    #   if false (default): behavior is not changed
    #   if true: self.mc_version will be updated to  latest version
    def latest_mc_version(self, update_used_version=False):
        print("Checking PaperMC's latest supported minecraft version!")
        latest_request = requests.get(PAPER_API_URL)
        if latest_request.status_code != 200:
            self.mc_version_latest = None
            print("Could not check latest supported version (CODE {})".format(latest_request.status_code))
            return
        latest_version = latest_request.json()['versions'][0]
        print("Latest supported minecraft version is {}".format(latest_version))
        self.mc_version_latest = latest_version
        if update_used_version and latest_version is not None:
            print("Setting currently used version to {}".format(latest_version))
            self.mc_version = latest_version
        return latest_version

    # Requests for latest released PaperMC build for given version
    # and returns it
    #
    # Without parameter, self.mc_version will be used
    def latest_paper_build(self, mc_version=None):
        if mc_version is None:
            mc_version = self.mc_version
        build_request = requests.get("{}/{}".format(PAPER_API_URL, mc_version))
        if build_request.status_code != 200:
            return None
        build_latest = build_request.json()["builds"]["latest"]
        return build_latest

    # Check if given build for given version exist
    #
    # Without parameters:
    #   self.mc_version -> mc_version
    #   latest_paper_build(mc_version) -> build
    def build_check(self, mc_version=None, build=None):
        if mc_version is None:
            mc_version = self.mc_version
        if build is None:
            build = self.latest_paper_build(mc_version)
        print("Checking existence of build: {}/{}".format(mc_version, build))
        check_request = requests.get("{}/{}/{}".format(PAPER_API_URL, mc_version, build))
        # PaperMC API returns code 404 for missing builds
        if check_request.status_code != 200:
            print("Build does not exist!")
            return False
        print("Build exist!")
        return True

    # TODO: download build
    # TODO: setting for delete older files
    # TODO: INI configuration
    # TODO: change behavior from ARGV
    # TODO: cmd args override -> INI cfg that override -> program constants
    # TODO: maybe something else DUNNO LOL


if __name__ == '__main__':
    updater = Updater()
    updater.latest_mc_version(True)
    updater.build_check()
    exit(0)

    req = requests.get("{}/{}/".format(PAPER_API_URL, PAPER_MC_VERSION))
    if req.status_code == 200:
        latest = req.json()["builds"]["latest"]
        files = sorted(glob.glob("paper-*"), reverse=True)
        current = files[0][6:-4] if len(files) > 0 else None
        if latest != current:
            print("Server update found: {} -> {}".format(current, latest))
            latest.replace("-", "/");
            print("{}/{}/{}/download".format(PAPER_API_URL, PAPER_MC_VERSION, latest))
            new = requests.get("{}/{}/{}/download".format(PAPER_API_URL, PAPER_MC_VERSION, latest))
            with open("paper-{}.jar".format(latest), "wb") as f:
                f.write(new.content)
            if current is not None:
                os.remove(files[0])
        else:
            print("Server is up to date")
