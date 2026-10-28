console.log("JavaScript is working!");


/* =========================
   LIVE STUDENT SEARCH
   ========================= */

const searchInput = document.getElementById("student-search");

if (searchInput) {

    let searchTimer;

    searchInput.addEventListener("input", function () {

        clearTimeout(searchTimer);

        searchTimer = setTimeout(function () {

            const searchValue = searchInput.value.trim();

            const url = new URL(window.location.href);

            if (searchValue) {
                url.searchParams.set("search", searchValue);
            } else {
                url.searchParams.delete("search");
            }

            // Start from page 1 whenever search changes
            url.searchParams.delete("page");

            window.location.href = url.toString();

        }, 300);

    });

}


/* =========================
   STUDENT FORM MARKS CHECK
   ========================= */

const studentForm = document.getElementById("student-form");

if (studentForm) {

    studentForm.addEventListener("submit", function (event) {

        const marksInput = document.getElementById("id_marks");

        if (!marksInput) {
            return;
        }

        const marks = parseFloat(marksInput.value);

        if (marks < 0 || marks > 100) {

            event.preventDefault();

            alert("Marks must be between 0 and 100.");

        }

    });

}