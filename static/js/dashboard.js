const settingsIcon = document.getElementById("settingsIcon");
const settingsOverlay = document.getElementById("settingsOverlay");
const settingsContainer = document.getElementById("settingsContainer");

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