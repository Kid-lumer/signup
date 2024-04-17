function validateSignUpForm() {
    var username = document.getElementById('username').value.trim();
    var email = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;
  
    // Basic validation
    if (username === '' || email === '' || password === '' || confirmPassword === '') {
        alert('All fields are required');
        return false;
    }
   
  }