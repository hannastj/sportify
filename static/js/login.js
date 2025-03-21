document.addEventListener('DOMContentLoaded', function() {
    // Select the registration form
    const registerForm = document.querySelector('form[input[name="register"]]');
    const errorContainer = document.createElement('div');
    errorContainer.classList.add('error-messages');
    registerForm.prepend(errorContainer);
  
    registerForm.addEventListener('submit', function(event) {
      // Clear previous error messages
      errorContainer.innerHTML = '';
      let errors = [];
  
      // Example: Check if the email field is valid
      const emailField = registerForm.querySelector('input[name="email"]');
      if (!emailField.value.includes('@')) {
        errors.push("Please enter a valid email address.");
      }
      
      // Check if the password meets a minimum length
      const passwordField = registerForm.querySelector('input[name="password1"]');
      if (passwordField.value.length < 8) {
        errors.push("Password must be at least 8 characters long.");
      }
      
      // Add any additional validations here as needed
  
      // If there are errors, prevent form submission and display them
      if (errors.length > 0) {
        event.preventDefault(); // Stop form from submitting
        errors.forEach(function(error) {
          const p = document.createElement('p');
          p.textContent = error;
          p.style.color = 'red'; // Style as needed
          errorContainer.appendChild(p);
        });
      }
    });
  });
  