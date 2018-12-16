"use strict";

console.log("Interactivity Loaded")

const bothButton = document.getElementById("show-both");
const noteButton = document.getElementById("show-notes");
const codeButton = document.getElementById("show-source");

const markdownCells = document.getElementsByClassName("markdown");
const codeCells = document.getElementsByClassName("code");

function hideCells(cells) {

    for (let i = 0; i < cells.length; i++) {
        const classList = cells[i].classList;

        if (classList.contains("is-visible")) {
            classList.remove("is-visible");
        }

        if (!classList.contains("is-hidden")) {
            classList.add("is-hidden");
        }

    }
}

function showCells(cells) {

    for (let i = 0; i < cells.length; i++) {
        const classList = cells[i].classList;

        if (classList.contains("is-hidden")) {
            classList.remove("is-hidden");
        }

        if (!classList.contains("is-visible")) {
            classList.add("is-visible");
        }

    }
}

bothButton.addEventListener("click", function() {
    showCells(codeCells);
    showCells(markdownCells);
});

noteButton.addEventListener("click", function() {
    hideCells(codeCells);
    showCells(markdownCells);
});

codeButton.addEventListener("click", function() {
    showCells(codeCells);
    hideCells(markdownCells);
});
