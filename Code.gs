const FILE_ID = "FILE ID HERE";

// only run once to get the file ID of the file that will store the data
// source: https://developers.google.com/apps-script/reference/drive/file-iterator
function findFileId(){
  let files = DriveApp.getFilesByName("data.csv");
  while (files.hasNext()) {
    const file = files.next();
    Logger.log(file.getId());
  }
}

/**
 * function that handles an incoming POST request with the new data from the latest snapshot
 * e.postData.contents contains the request body
 * The request body will be an object with a single attribute, snapshot 
 * snapshot points to the new rows of the csv file as a string, ending with a newline
 */
function doPost(e) {
  // 1. open the file: https://developers.google.com/apps-script/reference/drive/drive-app#getfilebyidid
  let file = DriveApp.getFileById(FILE_ID);
  // 2. read its contents
  // getBlob() https://developers.google.com/apps-script/reference/drive/file#getAs(String)
  // getDataAsString() https://developers.google.com/apps-script/reference/base/blob.html#getdataasstring
  let content = file.getBlob().getDataAsString();
  // 3. add the new contents
  let requestBody = JSON.parse(e.postData.contents);
  content += requestBody.snapshot;
  // 4. save the file https://developers.google.com/apps-script/reference/drive/file#setContent(String)
  file.setContent(content); 
}
