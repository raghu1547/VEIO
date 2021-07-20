const form = document.getElementById("rl");
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password1");
const password2 = document.getElementById("password2");

form.addEventListener("submit", (e) => {
  // checkInputs();
  checkInputs();
  if (document.querySelectorAll(".form-group.success small").length !== 7)
    e.preventDefault();
});

function checkSubmit() {
  console.log(form.children);
}
username.addEventListener("keyup", () => {
  if (!isUsername(username.value)) {
    setErrorFor(
      username,
      "containa atleast one Capital letter,alpha numeric,special character with no spaces and atleast 8 character length"
    );
  } else {
    checkUser();
  }
});
function checkUser() {
  //   console.log($("input[name=csrfmiddlewaretoken]").val());
  $.ajax({
    type: "POST",
    url: "/accounts/checkUser/",
    data: {
      user: username.value,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").prop("value"),
    },
    dataType: "json",
    success: function (data) {
      if (data.is_success) {
        setSuccessFor(username);
      } else {
        setErrorFor(username, "Username is unavailable");
      }
    },
  });
}
function checkInputs() {
  // trim to remove the whitespaces
  const usernameValue = username.value.trim();
  const emailValue = email.value.trim();
  const passwordValue = password.value.trim();
  const password2Value = password2.value.trim();

  setSuccessFor(document.getElementById("first-name"));
  setSuccessFor(document.getElementById("last-name"));
  setSuccessFor(document.getElementById("phoneno"));

  if (!isUsername(usernameValue)) {
    setErrorFor(
      username,
      "containa atleast one Capital letter,alpha numeric,special character with no spaces and atleast 8 character length"
    );
  } else {
    setSuccessFor(username);
  }

  if (!isEmail(emailValue)) {
    setErrorFor(email, "Not a valid email");
  } else {
    setSuccessFor(email);
  }

  if (!ispassword(passwordValue)) {
    setErrorFor(
      password,
      "Password should contain atleast one capital letter,digit,small letter and no spaces with atleast 8 characters"
    );
  } else {
    setSuccessFor(password);
  }

  if (passwordValue !== password2Value) {
    setErrorFor(password2, "Passwords does not match");
  } else {
    setSuccessFor(password2);
  }
}

function setErrorFor(input, message) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  formControl.className = "form-group error";
  small.innerText = message;
}

function setSuccessFor(input) {
  const formControl = input.parentElement;
  formControl.className = "form-group success";
}

function isEmail(email) {
  re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}
function isUsername(username) {
  re = /^((?=.*\d)(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,})$/;
  return re.test(username);
}
function ispassword(password) {
  re = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{8,}$/;
  return re.test(password);
}
