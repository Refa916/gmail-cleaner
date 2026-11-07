/**
 * Creates a copy of the configured Google Sheets template in the destination
 * Drive folder and displays a link to the new spreadsheet.
 *
 * Configure TEMPLATE_SPREADSHEET_ID and DESTINATION_FOLDER_ID in the Apps
 * Script project's Script Properties before deploying the web app.
 */
function doGet() {
  try {
    var createdFile = createSpreadsheetCopy_();
    var url = createdFile.getUrl();
    var html = '<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">' +
      '<title>Spreadsheet ready</title></head><body style="font:16px Arial,sans-serif;max-width:640px;margin:48px auto;padding:0 16px">' +
      '<h1>Your spreadsheet is ready</h1><p><a href="' + escapeHtml_(url) + '" target="_blank" rel="noopener">Open the new spreadsheet</a></p>' +
      '<p>You can close this page when you are done.</p></body></html>';
    return HtmlService.createHtmlOutput(html).setTitle('Spreadsheet ready');
  } catch (error) {
    var message = error && error.message ? error.message : String(error);
    var errorHtml = '<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">' +
      '<title>Could not create spreadsheet</title></head><body style="font:16px Arial,sans-serif;max-width:640px;margin:48px auto;padding:0 16px">' +
      '<h1>Could not create spreadsheet</h1><p>' + escapeHtml_(message) + '</p></body></html>';
    return HtmlService.createHtmlOutput(errorHtml).setTitle('Spreadsheet creation failed');
  }
}

function createSpreadsheetCopy_() {
  var properties = PropertiesService.getScriptProperties();
  var templateId = properties.getProperty('TEMPLATE_SPREADSHEET_ID');
  var folderId = properties.getProperty('DESTINATION_FOLDER_ID');

  if (!templateId || !folderId) {
    throw new Error('Set TEMPLATE_SPREADSHEET_ID and DESTINATION_FOLDER_ID in Script Properties.');
  }

  var template = DriveApp.getFileById(templateId);
  if (template.getMimeType() !== MimeType.GOOGLE_SHEETS) {
    throw new Error('The configured template must be a Google Sheets file.');
  }
  var destination = DriveApp.getFolderById(folderId);
  var timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd-HHmmss');
  var uniqueSuffix = Utilities.getUuid().substring(0, 8);
  var copyName = 'Spreadsheet - ' + timestamp + ' - ' + uniqueSuffix;

  var copy = template.makeCopy(copyName, destination);
  // This intentionally grants edit access to anyone who obtains the link.
  copy.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
  return copy;
}

function escapeHtml_(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
