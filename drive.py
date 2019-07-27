from googleapiclient.discovery import build

def BuildDrive(creds):
    """Creates a client for Drive API.

    :param creds: Google API credentials.
    :return: Drive API client.
    """
    return build('drive', 'v3', credentials=creds)


def GetModificationTime(service, file_id):
    """Creates modification time.

    :param service: Drive API client.
    :param file_id: ID of file on drive.
    :return: A string with modification date and time.
    """
    results = service.files().get(
       fileId=file_id, fields="modifiedTime").execute()
    return results.get("modifiedTime", None)



