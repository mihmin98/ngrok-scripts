import requests
import json

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive, GoogleDriveFile


def upload_file(drive: GoogleDrive, content):
    file_list = drive.ListFile(
        {
            "q": "title = '.ngrok_url' and 'root' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed != true"
        }
    ).GetList()

    f = None
    if len(file_list) < 1:
        f = drive.CreateFile({"title": ".ngrok_url"})
    else:
        f = file_list[0]

    f.SetContentString(content)
    f.Upload()

    return f


if __name__ == "__main__":

    content = dict()
    content["online"] = False

    try:
        r = requests.get("http://127.0.0.1:4040/api/tunnels")

        if r.ok:
            json_obj = json.loads(r.content)
            content["online"] = True
            content["ngrok"] = json_obj
    except:
        print("error get links")

    # TODO: Check if user is already logged in
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        drive = GoogleDrive(gauth)

        upload_file(drive, json.dumps(content))
    except:
        print("error drive")
