import requests
import os
import glob

PAPER_API_URL = "https://papermc.io/api/v1/paper"
PAPER_MC_VERSION = "1.13.2"

if __name__ == '__main__':
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
