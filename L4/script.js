let email = document.querySelector("#Email");
let password = document.querySelector("#Password");
let check = document.querySelector("#Check");

const isUpperCase = (string) => /^[A-Z]*$/.test(string);
const isLowerCase = (string) => /^[a-z]*$/.test(string);
const isNumberValue = (string) => /^[0-9]*$/.test(string);

let onChangeEmail = function(event) {
  let message = "Użyj znaku \"@\" w adresie email! ";
  let isError = true;
  for (let letter of event.target.value) {
    if (letter == '@') {
      isError = false;
      break;

    }

  }

  if (isError) {
    alert(message);

  }

}

let onChangePassword = function(event) {
  let message = "Hasło jest nie poprawne. ";
  let isUpper = false;
  let isLower = false;
  let isNumber = false;
  let isLength = false;
  let isError = false;
  if (event.target.value.length >= 8) {
    isLength = true;

  }
  for (let letter of event.target.value) {
    if (isUpperCase(letter)) {
      isUpper = true;

    }
    else if (isLowerCase(letter)) {
      isLower = true;

    }
    else if (isNumberValue(letter)) {
      isNumber = true;

    }

  }

  if (!isLength) {
    isError = true;
    message += "Hasło jest zbyt krótkie. ";

  }
  if (!isUpper) {
    isError = true;
    message += "Brakuje dużego znaku. ";

  }
  if (!isLower) {
    isError = true;
    message += "Brakuje małego znaku. ";

  }
  if (!isNumber) {
    isError = true;
    message += "Brakuje liczby. ";

  }

  if (isError) {
    alert(message);

  }

}

let onChangeCheck = function(event) {
  console.log(event.target.checked);

}

email.addEventListener("change", onChangeEmail);
password.addEventListener("change", onChangePassword);
check.addEventListener("change", onChangeCheck);
email.addEventListener("blur", onChangeEmail);
password.addEventListener("blur", onChangePassword);
check.addEventListener("blur", onChangeCheck);
