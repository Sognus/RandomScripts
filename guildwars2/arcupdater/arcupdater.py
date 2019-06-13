from requests.exceptions import MissingSchema
import os
import hashlib
import requests


class ArcUpdater:
    MD5_FILE = "d3d9.dll.md5sum"

    def __init__(self, args):
        self.args = args
        self.MD5_URL = self.args.arc_url + self.MD5_FILE
        self.update()

    def update(self):
        # Update D3D9
        if self.local_md5(os.path.join(self.args.arc_location, "d3d9.dll")) != self.remote_md5():
            print("ARCDPS UPDATE AVAILABLE!")
            print("DOWNLOADING ARCDPS UPDATE...")
            text = "ARCPDPS UPDATED!" if self.download(self.args.arc_url + "d3d9.dll") else "ARCDPS UPDATE FAILED"
            print(text)
            print()
        else:
            print("ARCDPS IS UP TO DATE!")
            print()
        # Update Buildtemplates
        if self.args.arc_templates:
            print("DOWNLOADING ARCPDPS BUILD TEMPLATES...")
            self.download(self.args.arc_url + "buildtemplates/d3d9_arcdps_buildtemplates.dll")
            text = "ARCPDPS BUILD TEMPLATES UPDATED!" if self.download(
                self.args.arc_url + "d3d9.dll") else "ARCDPS BUILD TEMPLATES UPDATE FAILED"
            print(text)
            print()
        # Update Extras
        if self.args.arc_templates:
            print("DOWNLOADING ARCPDPS EXTRAS...")
            self.download(self.args.arc_url + "extras/d3d9_arcdps_extras.dll")
            text = "ARCPDPS EXTRAS UPDATED!" if self.download(
                self.args.arc_url + "d3d9.dll") else "ARCDPS EXTRAS UPDATE FAILED"
            print(text)
            print()

    # Downloads file from url
    def download(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                name = url.rsplit("/", 1)[-1]
                with open(os.path.join(self.args.arc_location, name), 'wb') as file:
                    file.write(r.content)
                return True
        except MissingSchema as error:
            return False

    # Returns last modified for remote file or None
    def remote_last_modified(self, url):
        try:
            r = requests.head(url)
            if r.status_code == 200:
                return r.headers["Last-Modified"]
        except MissingSchema:
            pass
        return None

    # Returns md5 of local file
    def local_md5(self, path):
        if not os.path.isfile(path):
            return None
        with open(path, 'rb') as file:
            return hashlib.md5(file.read()).hexdigest()

    # Returns remote md5 or None
    def remote_md5(self, url=None):
        d3d9_md5_flag = False
        # Default value
        if url is None or url == self.MD5_URL:
            url = self.MD5_URL
            d3d9_md5_flag = True
        try:
            r = requests.get(url)
            if r.status_code == 200:
                if d3d9_md5_flag:
                    return r.text.split(' ')[0]
                else:
                    return hashlib.md5(r.content).hexdigest()
        except (MissingSchema, TypeError) as error:
            pass
        return None
