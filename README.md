# Google Sheets Template Generator

A Google Apps Script web app that copies a Google Sheets template from Google Drive, saves the copy in a chosen folder, enables **anyone with the link to edit**, and displays a clickable link to the new spreadsheet.

## Setup

1. Open [Google Apps Script](https://script.google.com/) and create a project.
2. Add the contents of `Code.gs` to the project.
3. In **Project Settings → Script Properties**, add:
   - `TEMPLATE_SPREADSHEET_ID`: the ID of the source Google Sheets template.
   - `DESTINATION_FOLDER_ID`: the ID of the Drive folder where copies should be saved.
4. Deploy the project as a **Web app**. Choose the account that should own/create the copies under **Execute as**, and configure who can access the web app.
5. Authorize the requested Google Drive permissions, then open the deployment URL.

The template ID is the portion after `/spreadsheets/d/` in its URL. The destination folder ID is the portion after `/folders/` in its URL. The configured template must be a native Google Sheets file.

## Behavior and sharing warning

Each web app request creates a fresh copy. The copy name includes a timestamp and a random suffix to keep names unique. The script then sets the copy's sharing to **Anyone with the link — Editor** and returns its URL. This makes the spreadsheet editable by anyone who gets the link; do not use this setting for sensitive data. Google Workspace administrators may prohibit public link sharing, in which case creation will report an error.

The account selected under **Execute as** needs access to both the template and destination folder. Restrict web app access appropriately: anyone allowed to run it may cause a new copy to be created each time they open the app.
