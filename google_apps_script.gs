// Google Apps Script: doGet/doPost separados para login (leitura) e register (escrita)

function doPost(e) {
  // log da chamada
  logCall('POST', (e && e.parameter && e.parameter.action) || (e && e.postData && 'POST_BODY') || 'unknown', {body: e && e.postData && e.postData.contents});
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
  // log da chamada GET
  logCall('GET', (e && e.parameter && e.parameter.action) || 'unknown', e && e.parameter);
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

  if (!data.nome || !data.matricula || !data.email || typeof data.senha === 'undefined') {
    return jsonResponse({ success: false, message: "Campos incompletos." });
  }

  const matricula = String(data.matricula).trim();

  // Evitar registro duplicado pela mesma matrícula
  const values = sheet.getDataRange().getValues();
  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    if (String(row[1]).trim() === matricula) {
      return jsonResponse({ success: false, message: "ALREADY_EXISTS" });
    }
  }

  // Guarda a senha AS-IS (texto puro). ⚠️ inseguro
  sheet.appendRow([
    String(data.nome),
    matricula,
    String(data.email),
    String(data.senha),
    new Date()
  ]);

  return jsonResponse({ success: true, message: "REGISTER_OK" });
}

function handleLogin(params) {
  const matricula = params.matricula;
  const senha = params.senha; // texto puro

  if (!matricula || typeof senha === 'undefined') {
    return jsonResponse({ success: false, message: "Parâmetros incompletos." });
  }

  const sheet = getSheet();
  const values = sheet.getDataRange().getValues();

  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    const matricula_sheet = String(row[1]);
    const senha_sheet = String(row[3]);

    if (matricula_sheet == String(matricula) && senha_sheet == String(senha)) {
      return jsonResponse({
        success: true,
        message: "LOGIN_OK",
        nome: row[0],
        email: row[2]
      });
    }
  }

  return jsonResponse({ success: false, message: "LOGIN_FAIL" });
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Usuarios");
  if (!sheet) {
    sheet = ss.insertSheet("Usuarios");
    sheet.appendRow(["Nome", "Matricula", "Email", "Senha", "Data"]);
  }
  return sheet;
}

/*
  Função de logging: cria/usa aba 'Logs' para registrar chamadas
  Isso ajuda depurar se GET/POST estão sendo chamados e com quais parâmetros.
*/
function logCall(method, action, params) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let logSheet = ss.getSheetByName('Logs');
    if (!logSheet) {
      logSheet = ss.insertSheet('Logs');
      logSheet.appendRow(['Timestamp','Method','Action','Params']);
    }
    const ts = new Date();
    const p = JSON.stringify(params || {});
    logSheet.appendRow([ts, method, action, p]);
  } catch (err) {
    // falha de logging não deve quebrar fluxo
    console.error('logCall error:', err);
  }
}
