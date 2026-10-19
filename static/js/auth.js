const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");


loginForm.addEventListener('submit', async function (event){
    event.preventDefault();

    const loginData = new FormData(loginForm);

    const response = await fetch("/login", {
        method: "POST",
        body: loginData
    });

    const result = await response.json();

    if (!response.ok){
        alert("User not found");
    }
    else{
        alert(result.message);
    }
})