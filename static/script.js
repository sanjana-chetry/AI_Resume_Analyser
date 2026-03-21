
/* Welcome Animation 
   Z falls first, then C (200ms later), then V (400ms later).
   After V lands, tagline fades in.
   After tagline shows, overlay fades out and main content fades in.
*/
(function runWelcome() {
    const overlay   = document.getElementById("welcome-overlay");
    const mainContent = document.getElementById("main-content");
    const tagline   = document.getElementById("welcome-tagline");
    const letters   = [
        document.getElementById("wl-z"),
        document.getElementById("wl-c"),
        document.getElementById("wl-v"),
    ];

    if (!overlay || !mainContent) return;

    // Animate each letter with a stagger
    letters.forEach((el, i) => {
        if (!el) return;
        setTimeout(() => {
            el.style.animation = "letterFall 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards";
        }, i * 220); // 0ms, 220ms, 440ms
    });

    // Show tagline after all letters have landed
    setTimeout(() => {
        if (tagline) tagline.classList.add("show");
    }, 440 + 700 + 200); 

    // Fade out overlay and reveal page
    setTimeout(() => {
        overlay.classList.add("hide");
        setTimeout(() => {
            overlay.style.display = "none";
            mainContent.classList.add("visible");
        }, 800);
    }, 440 + 700 + 900); // after tagline has been visible ~700ms
})();


(function navScroll() {
    const nav = document.getElementById("mainNav");
    if (!nav) return;

    let lastScrollY = 0;

    window.addEventListener("scroll", () => {
        const current = window.scrollY;
        if (current > lastScrollY && current > 80) {
            // Scrolling down — hide nav
            nav.classList.add("nav-hidden");
        } else {
            // Scrolling up — show nav
            nav.classList.remove("nav-hidden");
        }
        lastScrollY = current;
    }, { passive: true });
})();


/* Mobile Nav Toggle */
const navToggle = document.getElementById("navToggle");
const navDrawer = document.getElementById("navDrawer");

if (navToggle && navDrawer) {
    navToggle.addEventListener("click", () => navDrawer.classList.toggle("open"));
    document.addEventListener("click", e => {
        if (!navToggle.contains(e.target) && !navDrawer.contains(e.target))
            navDrawer.classList.remove("open");
    });
}


/* Theme Toggle 
   Saves preference to localStorage so it persists across pages.
*/
function applyTheme(light) {
    document.body.classList.toggle("light", light);
    localStorage.setItem("zcv-theme", light ? "light" : "dark");
    // Sun icon shown in dark mode 
    // Moon icon shown in light mode 
    const sun  = document.getElementById("iconSun");
    const moon = document.getElementById("iconMoon");
    if (sun)  sun.style.display  = light ? "none"  : "inline";
    if (moon) moon.style.display = light ? "inline" : "none";
    const mob = document.getElementById("mobileThemeToggle");
    if (mob) mob.textContent = light ? "Switch to Dark" : "Switch to Light";
}

// Apply saved theme — runs after DOM is ready
window.addEventListener("DOMContentLoaded", () => {
    applyTheme(localStorage.getItem("zcv-theme") === "light");

    const themeBtn = document.getElementById("themeToggle");
    const mobTheme = document.getElementById("mobileThemeToggle");

    if (themeBtn) themeBtn.addEventListener("click", () =>
        applyTheme(!document.body.classList.contains("light")));
    if (mobTheme) mobTheme.addEventListener("click", e => {
        e.preventDefault();
        applyTheme(!document.body.classList.contains("light"));
    });
});


/* File Upload */
const fileInput      = document.getElementById("resume-input");
const uploadBox      = document.getElementById("uploadBox");
const uploadSubtitle = document.getElementById("uploadSubtitle");
const roleSection    = document.getElementById("roleSection");
const roleSelect     = document.getElementById("roleSelect");
const analyseBtn     = document.getElementById("analyseBtn");
const uploadForm     = document.getElementById("uploadForm");

function onFileSelected(file) {
    if (!file) return;
    uploadSubtitle.textContent = file.name + " selected";
    uploadBox.classList.add("active");
    roleSection.classList.add("show");
    roleSelect.disabled = false;
}

if (fileInput) {
    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) onFileSelected(fileInput.files[0]);
    });
}


/* Drag and Drop */
if (uploadBox) {
    uploadBox.addEventListener("dragover",  e => { e.preventDefault(); uploadBox.classList.add("dragover"); });
    uploadBox.addEventListener("dragleave", ()  => uploadBox.classList.remove("dragover"));
    uploadBox.addEventListener("drop", e => {
        e.preventDefault();
        uploadBox.classList.remove("dragover");
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            onFileSelected(e.dataTransfer.files[0]);
        }
    });
}


/* Role Selection */
if (roleSelect) {
    roleSelect.addEventListener("change", () => {
        const enabled = roleSelect.value !== "";
        analyseBtn.disabled = !enabled;
        analyseBtn.classList.toggle("enabled", enabled);
    });
}


/* Form Submit — show loading  */
if (uploadForm) {
    uploadForm.addEventListener("submit", () => {
        document.getElementById("btnText").textContent = "Analysing...";
        analyseBtn.disabled = true;
        uploadBox.classList.add("loading");

        const status = document.createElement("p");
        status.textContent = "Validating and analysing your resume...";
        status.style.cssText = "font-size:0.82rem;color:rgba(238,239,254,0.45);text-align:center;margin-top:4px;";
        roleSection.after(status);
    });
}


/* Auto-dismiss error message */
window.addEventListener("load", () => {
    const err = document.getElementById("errorMessage");
    if (err) {
        setTimeout(() => { err.style.transition = "opacity 0.5s ease"; err.style.opacity = "0"; }, 5500);
        setTimeout(() => { if (err) err.remove(); }, 5500);
    }
});
