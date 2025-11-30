function toggleForm(type) {
    const loginSection = document.getElementById('loginFormSection');
    const signupSection = document.getElementById('signupFormSection');
    const leftTitle = document.getElementById('leftTitle');
    const leftDesc = document.getElementById('leftDesc');

    if (type === 'signup') {
        loginSection.classList.add('d-none');
        signupSection.classList.remove('d-none');
        leftTitle.innerText = "Create Account";
        leftDesc.innerText = "Share your artwork and get projects today!";
    } else {
        signupSection.classList.add('d-none');
        loginSection.classList.remove('d-none');
        leftTitle.innerText = "Welcome Back";
        leftDesc.innerText = "To keep connected with us please login with your personal info";
    }
}