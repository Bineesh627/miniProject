document.getElementById('registerForm').addEventListener('submit', function(event) {
  const pass = document.getElementById('pass').value;
  const confirmPass = document.getElementById('confirmPass').value;

  if (pass !== confirmPass) {
    alert('Passwords do not match');
    event.preventDefault();
  }
});