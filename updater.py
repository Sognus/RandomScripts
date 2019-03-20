import requests
import os
import glob

PAPER_API_URL = "https://papermc.io/api/v1/paper"
PAPER_MC_VERSION = "1.13.2"

if __name__ == '__main__':
    req = requests.get("https://papermc.io/api/v1/paper/1.13.2/")
    if req.status_code == 200:
        latest = req.json()["builds"]["latest"]
        files = sorted(glob.glob("paper-*"), reverse=True)
        current = files[0][6:-4] if len(files) > 0 else None
        print(latest)
        print(current)
        if latest != current:
            print(f"Server update found: {current} -> {latest}")
            latest.replace("-", "/");
            print(f"{PAPER_API_URL}/{PAPER_MC_VERSION}/{latest}/download")
            new = requests.get(f"{PAPER_API_URL}/{PAPER_MC_VERSION}/{latest}/download")
            with open(f"paper-{latest}.jar", "wb") as f:
                f.write(new.content)
            if current is not None:
                os.remove(files[0])
        else:
            print("Server is up to date")
