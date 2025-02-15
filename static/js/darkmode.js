let darkmode = localStorage.getItem('darkmode');
const themeSwitch = document.getElementById('theme-switch');

const enableDarkMode = () => {
    document.body.classList.add("darkmode");
    localStorage.setItem('darkmode', 't');
}

const disableDarkMode = () => {
    document.body.classList.remove("darkmode");
    localStorage.setItem("darkmode", null);
}

if (darkmode === 't') enableDarkMode();

themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem("darkmode");
    darkmode === 't' ? disableDarkMode() : enableDarkMode();
}) 
