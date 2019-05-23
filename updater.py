import requests
import argparse
import os
import glob

# Constants
PAPER_API_URL = "https://papermc.io/api/v1/paper"
PAPER_MC_VERSION = "1.13.2"


# TODO: setting for delete older files
#   probably delete all other files in paper-VERSION-BUILD.jar format
#   setting to rename paper-VERSION-BUILD.jar to paper.jar
#   when rename will be set, update anyway, if not check if server is up to date
#   maybe I will just save info of latest downloaded version into file


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--minecraft', help="Minecraft version", metavar="minecraft version")
    parser.add_argument("--latest", "-l", help="Use latest build", action="store_true", default=True)
    parser.add_argument("--latest-version", "-L", help="Use latest minecraft version", action="store_true", default=True)
    parser.add_argument("--build", "-b", help="Specify PaperMC build", choices=["latest", int], metavar="[int|latest]")
    return parser.parse_args()

class Updater:

    #
    # minecraft_version:    (IE. 1.14.1)                          cannot be used with latest_version (version >latest_v)
    # build:                PaperMC build (dependant on version)  cannot be used with latest (build > latest_build)
    # latest_build:         Use latest paperMC build              cannot be used with build  (build > latest_build)
    # latest_version:       Use latest minecraft version          cannot be used with minecraft_version
    def __init__(self, minecraft_version=None, build=None, latest_build=True, latest_version=True):
        # Latest minecraft version (IE. 1.13.2)
        self.mc_version_latest = None
        # Current used minecraft version
        self.mc_version = None
        # Prepare values for input decode
        self.use_latest_build = latest_build
        self.use_latest_version = latest_version
        self.use_build = None
        # Take inputs and parse them
        self.decode_input(minecraft_version, build, latest_build, latest_version)

    def job(self):
        self.download_build(self.mc_version, self.use_build)

    def decode_input(self, minecraft_version, build, latest_build, latest_version):
        # If none of required values is set, raise error
        if minecraft_version is None and latest_version is False:
            raise ValueError("Atleast of minecraft version or latest version flag must be set!")
        # If none of required values is set, raise error
        if build is None and latest_build is False:
            raise ValueError("Atleast of PaperMC build or latest build flag must be set!")

        # If version is specified and is valid, set latest flag False
        if minecraft_version is not None and self.version_check(minecraft_version):
            self.use_latest_version = False
            self.mc_version = minecraft_version
        else:
            self.use_latest_version = True
            self.mc_version = self.latest_mc_version()

        # If build is specified and is valid, set latest flag False
        if build is not None and self.build_check(self.mc_version):
            self.use_latest_build = False
            self.use_build = build
        else:
            self.use_latest_build = True
            self.use_build = self.latest_paper_build(self.mc_version)

        print("Updater is set to download {}/{}".format(self.mc_version, self.use_build))

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

    def version_check(self, mc_version):
        version_request = requests.get(PAPER_API_URL)
        print("Checking PaperMC's support for minecraft version {}".format(mc_version))
        if version_request.status_code != 200:
            print("Check failed! (CODE = {})".format(version_request.status_code))
        version_json = version_request.json()["versions"]
        if mc_version not in version_json:
            print("Version {} is not supported!".format(mc_version))
            return False
        else:
            print("Version {} is supported!".format(mc_version))
            return True

    def download_build(self, mc_version=None, build=None):
        if mc_version is None:
            mc_version = self.mc_version
        if build is None:
            build = self.latest_paper_build(mc_version)
        download = requests.get("{}/{}/{}/download".format(PAPER_API_URL, mc_version, build))
        print("Downloading build {}/{}".format(mc_version, build))
        if download.status_code != 200:
            print("Build {}/{} could not be downloaded!".format(mc_version, build))
            return
        with open("paper-{}-{}.jar".format(mc_version, build), "wb") as f:
            f.write(download.content)
        print("PaperMC was downloaded to paper-{}-{}.jar".format(mc_version, build))


if __name__ == '__main__':
    args = setup_parser()
    print(args)

    updater = Updater(args.minecraft, args.build, args.latest, args.latest_version)
    updater.job()
    exit(0)

    '''
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
        '''
