import json
import sys

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def get_file(drive: GoogleDrive):
    file_list = drive.ListFile(
        {
            "q": "title = '.ngrok_url' and 'root' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed != true"
        }
    ).GetList()

    if len(file_list) > 0:
        content_string = file_list[0].GetContentString()
        return json.loads(content_string)
    else:
        return None


if __name__ == "__main__":
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    json_obj = get_file(drive)

    if json_obj is None:
        print("Error: File not found")
        sys.exit(0)

    if json_obj["online"] == True:
        ngrok_obj = json_obj["ngrok"]
        for tunnel in ngrok_obj["tunnels"]:
            print("%s: %s" % (tunnel["name"], tunnel["public_url"]))
