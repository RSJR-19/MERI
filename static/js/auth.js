const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const splashScreen = document.getElementById("splashScreen");
const getStartedScreen = document.getElementById("getStartedScreen");
const getStartedBtn = document.getElementById('getStartedBtn');
const logo = document.getElementById("logo");
const body = document.getElementById("body");
const loginP = document.getElementById("loginP");
const signupP = document.getElementById("signupP");
const loginScreen = document.getElementById("loginScreen");
const signupScreen = document.getElementById("signupScreen");
const emailLoginInput = document.getElementById("emailLoginInput");
const passwordLoginInput = document.getElementById('passwordLoginInput');
const usernameSignupInput = document.getElementById("usernameSignupInput");
const emailSignupInput = document.getElementById("emailSignupInput");
const passwordSignupInput = document.getElementById("passwordSignupInput");
const confirmPasswordSignupInput = document.getElementById("confirmPasswordSignupInput");

let usernameTimeout;

emailSignupInput.value = "";
passwordSignupInput.value = "";
usernameSignupInput.value = "";
emailSignupInput.value = "";
passwordSignupInput.value = "";
confirmPasswordSignupInput.value = "";

getStartedBtn.addEventListener('click', ()=>{
    getStartedScreen.classList.add("swipe");
    body.classList.add("reveal");
});

loginP.addEventListener('click', () => {
    emailLoginInput.value = "";
    passwordLoginInput.value = "";
    loginP.classList.remove("change");
    signupP.classList.remove("change");
    loginScreen.classList.remove("swipe");
});

signupP.addEventListener('click', () => {
    usernameSignupInput.value = "";
    emailSignupInput.value = "";
    passwordSignupInput.value = "";
    confirmPasswordSignupInput.value = "";
    loginP.classList.add("change");
    signupP.classList.add("change");
    loginScreen.classList.add("swipe");
});

setTimeout(()=>{
    splashScreen.classList.add("reveal");
    setTimeout(()=>{
        logo.classList.add("reveal");
        setTimeout(()=>{
            console.log("hi")
            splashScreen.classList.add("swipe");
        }, 1500)
    }, 550)

}, 200)


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

usernameSignupInput.addEventListener('input', ()=>{
    clearTimeout(usernameTimeout);

    usernameTimeout = setTimeout(async ()=>{
        const signupData = new FormData();
        signupData.append('username', usernameSignupInput.value);

        const response = await fetch('/check-username',{
            method: 'POST',
            body: signupData
        })

        const result = await response.json();

        if (!response.ok){
            alert(result.message)
        }
    }, 500);
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