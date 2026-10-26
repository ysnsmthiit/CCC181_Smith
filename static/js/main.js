// static/js/main.js
console.log("angOrderQ scripts loaded");

// 8a. Stop double joining
const joinForm = document.getElementById("join-form");
if (joinForm) {
    joinForm.addEventListener("submit", () => {
        const button = joinForm.querySelector("button[type=submit]");
        if (button) {
            button.disabled = true;
            button.textContent = "Getting your ticket…";
        }
    });
}
