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
        window.location.href = result.redirect;
    }
})

signupForm.addEventListener('submit', async function (event){
    event.preventDefault();

    const signupData = new FormData(signupForm);

    try{
        const response = await fetch("/signup", {
        method: "POST",
        body: signupData
    });


        const result = await response.json();

    if (!response.ok){
        alert(result.message);
        return
    }
    
    window.location.href = result.redirect;

} catch(error){
    console.error("Signup error:", error);
    alert("Something went wrong. Plsss Try again.")
}
})