$(document).ready(function() {
  $('#registerForm').on('submit', function(e) {
    e.preventDefault();
    var valid = true;

    // Clear errors
    $('.error').text('');

    // Username validation
    var username = $('#username').val().trim();
    if (!username || username.length < 3 || username.length > 30) {
      $('#usernameError').text('Username must be 3-30 characters');
      valid = false;
    } else if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
      $('#usernameError').text('Only letters, numbers, underscores, and hyphens allowed');
      valid = false;
    }

    // Email validation
    var email = $('#email').val().trim();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      $('#emailError').text('Please enter a valid email address');
      valid = false;
    }

    // Password validation
    var password = $('#password').val();
    if (!password || password.length < 8) {
      $('#passwordError').text('Password must be at least 8 characters');
      valid = false;
    } else if (!/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/[0-9]/.test(password)) {
      $('#passwordError').text('Password must include uppercase, lowercase, and a digit');
      valid = false;
    }

    // Age validation
    var age = parseInt($('#age').val(), 10);
    if (isNaN(age) || age < 1 || age > 120) {
      $('#ageError').text('Age must be a whole number between 1 and 120');
      valid = false;
    }

    if (valid) {
      $.ajax({
        url: '/api/register',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ username: username, email: email, password: password, age: age }),
        success: function(data) {
          $('#result').html('<p style="color:green;">Registration successful!</p>');
        },
        error: function(xhr) {
          var resp = xhr.responseJSON;
          if (resp && resp.errors) {
            $('#result').html('<p style="color:red;">' + resp.errors.map(function(e) { return e.message; }).join('<br>') + '</p>');
          }
        }
      });
    }
  });
});
