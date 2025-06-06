// Sign Up
if (document.getElementById("signupForm")) {
  document.getElementById("signupForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const mobile = document.getElementById("mobile").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const picFile = document.getElementById("profilePic").files[0];
    const profilePic = picFile ? await toBase64(picFile) : "";

    let users = JSON.parse(localStorage.getItem("users")) || {};
    if (users[email]) {
      return alert("User already exists!");
    }

    users[email] = { name, mobile, email, password, profilePic };
    localStorage.setItem("users", JSON.stringify(users));
    alert("Sign up successful!");
    window.location.href = "signin";
  });
}

// Sign In
if (document.getElementById("signinForm")) {
  document.getElementById("signinForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const users = JSON.parse(localStorage.getItem("users")) || {};
    if (users[email] && users[email].password === password) {
      localStorage.setItem("loggedInUser", email);
      alert("Login successful!");
      window.location.href = "index";
    } else {
      alert("Invalid credentials");
    }
  });
}

// Reset Password
if (document.getElementById("resetForm")) {
  document.getElementById("resetForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const newPassword = document.getElementById("newPassword").value;

    let users = JSON.parse(localStorage.getItem("users")) || {};
    if (!users[email]) {
      return alert("User not found!");
    }

    users[email].password = newPassword;
    localStorage.setItem("users", JSON.stringify(users));
    alert("Password reset successfully!");
    window.location.href = "signin";
  });
}

// Helper
function toBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
