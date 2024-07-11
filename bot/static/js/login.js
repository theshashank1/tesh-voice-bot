document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const usernameInput = document.querySelector('#username');
    const passwordInput = document.querySelector('#password');
    const usernameError = document.querySelector('#username-error');
    const passwordError = document.querySelector('#password-error');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = usernameInput.value;
        const password = passwordInput.value;

        // Validate username and password
        if (username === '') {
            usernameError.textContent = 'Username is required';
        } else {
            usernameError.textContent = '';
        }

        if (password === '') {
            passwordError.textContent = 'Password is required';
        } else {
            passwordError.textContent = '';
        }

        // Add your login logic here
        if (username!== '' && password!== '') {
            console.log(`Username: ${username}, Password: ${password}`);
            // Redirect to dashboard or show success message
        }
    });
});