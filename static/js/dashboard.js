const settingsIcon = document.getElementById("settingsIcon");
const settingsOverlay = document.getElementById("settingsOverlay");
const settingsContainer = document.getElementById("settingsContainer");
const logoutBtn = document.getElementById("logoutBtn");
const backBtn = document.getElementById("backBtn");
const logoutOverlay = document.getElementById("logoutOverlay");
const logoutPopup = document.getElementById("logoutPopup");
const notYetBtn = document.getElementById("notYetBtn");
const yesSirBtn = document.getElementById("yesSirBtn");


logoutOverlay.style.display = "none";
settingsOverlay.style.display = "none";

settingsIcon.addEventListener('click',()=>{
    settingsOverlay.style.display = "flex";
    setTimeout(()=>{
        settingsOverlay.classList.add("reveal");
        setTimeout(()=>{
            settingsContainer.classList.add("reveal");
        }, 100)
        
    }, 50)

})

backBtn.addEventListener('click', ()=>{
    settingsContainer.classList.remove("reveal");
    setTimeout(()=>{
        settingsOverlay.classList.remove("reveal");
        setTimeout(()=>{
            settingsOverlay.style.display = "none";
        }, 100)
    }, 300)
})

logoutBtn.addEventListener('click', ()=>{
    logoutOverlay.style.display = 'flex';
    setTimeout(()=>{
        logoutPopup.classList.add("reveal");
    }, 100)
})

notYetBtn.addEventListener('click', ()=>{
    logoutPopup.classList.remove('reveal');
    setTimeout(()=>{
        logoutOverlay.style.display = "none";
    }, 400)
})