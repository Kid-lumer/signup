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
  
    // Validate password format (at least one letter, one number, and one special character)
    var passwordPattern = /^(?=.[a-zA-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$/;
    if (!passwordPattern.test(password)) {
        alert('Password must contain at least 8 characters, including at least one letter, one number, and one special character.');
        return false;
    }
  
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return false;
    }
  
    // Additional validation logic can be added here (e.g., password strength, email format)
  
    // Form is valid
    return true;
  }