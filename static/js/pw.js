/* set up a password form */

const form = document.getElementById('password-form');
const passwordInput = document.getElementById('password');
const correctPassword = 'password123'; // Change this to the actual password you want to use

form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the form from submitting and refreshing the page

  const password = passwordInput.value;

  if (password === correctPassword) {
    window.location.href = '../management'; // Change this to the URL of your protected page
  } else {
    alert('Incorrect password. Please try again.'); // Display an error message
    passwordInput.value = ''; // Clear the password input field
  }
});
