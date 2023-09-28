// Format the copied PISA data.
function format_PISA_results() {
  let sheet = SpreadsheetApp.getActiveSheet();

  let rowIndex = 1;  // The starting row of a range.
  let colIndex = 1;  // The starting row of a column.
  let last_row = sheet.getLastRow();
  let last_col = sheet.getLastColumn();

  let range = sheet.getRange(rowIndex, colIndex, last_row, last_col);

  const searchString = "\\( .+?%\\)$";
  const replaceString = "";

  const textObject = range.createTextFinder(searchString).useRegularExpression(true);
  const results = textObject.findAll();

  //console.log("Number of matches to pattern : " + results.length);
  SpreadsheetApp
  .getUi()
  .alert("Number of matches to pattern [\\( .+?%\\)$] : " + results.length);

  // Show search results.
  if (results.length > 0) {
    let logs = "";
    for (let i = 0; i < results.length; i++) {
      let position = results[i].getA1Notation();
      let content = results[i].getValue();

      //console.log("Cell : " + position + ' => "' + content + '"');
      logs += "Cell : " + position + ' => "' + content + '"\n';
    }

    SpreadsheetApp.getUi().alert(logs);

    // Replace
    range.createTextFinder(searchString).useRegularExpression(true).replaceAllWith(replaceString);
  }
}


// Add menu to function called when the spreadsheet opens.
function onOpen() {
  SpreadsheetApp
  .getActiveSpreadsheet()
  .addMenu("一括修正", [
    { name: "データの数値化", functionName: "format_PISA_results" },
  ]);
}
