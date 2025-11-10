// Google Apps Script: doGet/doPost separados para login (leitura) e register (escrita)

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const action = data.action;

    if (action === "register") {
      return handleRegister(data);
    }

    return jsonResponse({
      success: false,
      message: "Invalid action for POST. Use action=register."
    });

  } catch (err) {
    return jsonResponse({
      success: false,
      message: "Erro no POST: " + err
    });
  }
}

function doGet(e) {
  try {
    const action = e.parameter.action;

    if (action === "login") {
      return handleLogin(e.parameter);
    }

    return jsonResponse({
      success: false,
      message: "Invalid action for GET. Use action=login."
    });

  } catch (err) {
    return jsonResponse({
      success: false,
      message: "Erro no GET: " + err
    });
  }
}

function handleRegister(data) {
  const sheet = getSheet();

  if (!data.nome || !data.matricula || !data.email || !data.senha) {
    return jsonResponse({ success: false, message: "Campos incompletos." });
  }

  sheet.appendRow([data.nome, data.matricula, data.email, data.senha, new Date()]);

  return jsonResponse({ success: true, message: "REGISTER_OK" });
}

function handleLogin(params) {
  const matricula = params.matricula;
  const senha = params.senha;

  if (!matricula || !senha) {
    return jsonResponse({ success: false, message: "Parâmetros incompletos." });
  }

  const sheet = getSheet();
  const values = sheet.getDataRange().getValues();

  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    if (row[1] == matricula && row[3] == senha) {
      return jsonResponse({ success: true, message: "LOGIN_OK", nome: row[0], email: row[2] });
    }
  }

  return jsonResponse({ success: false, message: "LOGIN_FAIL" });
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Usuarios");
  if (!sheet) {
    sheet = ss.insertSheet("Usuarios");
    sheet.appendRow(["Nome", "Matricula", "Email", "Senha_Hash", "Data"]);
  }
  return sheet;
}

