from googleapiclient.discovery import build



READ_RANGE = 'Sheet1!A2:A'
WRITE_RANGE = "Sheet1!B3:L"


def BuildService(creds):
    """Creates a client for Sheets API.

    :param creds: Google API credentials.
    :return: Sheets API client.
    """
    return build('sheets', 'v4', credentials=creds)


def ReadMovieNames(service, sheet_id):
    """Reads movie titles from a spreadsheet.

    :param service: Sheets API client.
    :param sheet_id: Id of spreadsheet.
    :return: List of movie titles.
    """
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=READ_RANGE).execute()
    values = result.get('values', [])
    result = []
    for row in values:
        result.append(row[0])
    return result


def WriteMovieInfo(info, service, sheet_id):
    """Writes movie table to spreadsheet.

    :param info: List of lists including movie ang rating information.
    :param service: Sheets API client.
    :param sheet_id: Id of spreadsheet.
    :return: Sheets API call result.
    """
    body = {
        "range": WRITE_RANGE,
        "majorDimension": "ROWS",
        "values": info,
    }
    sheet = service.spreadsheets()
    sheet.values().clear(spreadsheetId=sheet_id, range=WRITE_RANGE).execute()
    result = sheet.values().update(
        spreadsheetId=sheet_id, range=WRITE_RANGE,
        valueInputOption='USER_ENTERED', body=body).execute()
    return result


