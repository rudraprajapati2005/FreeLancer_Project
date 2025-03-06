document.addEventListener("DOMContentLoaded", function () {
    // Default active tab
    document.querySelector(".tab1-project-info").classList.add("active");
    document.querySelector(".tabs h3:first-child").classList.add("active");

    document.querySelectorAll(".tabs h3").forEach(tab => {
        tab.addEventListener("click", function () {
            document.querySelectorAll(".tabs h3").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab1-project-info, .tab2-project-proposals").forEach(content => content.classList.remove("active"));

            this.classList.add("active");
            if (this.innerText === "Details") {
                document.querySelector(".tab1-project-info").classList.add("active");
            } else {
                document.querySelector(".tab2-project-proposals").classList.add("active");
            }
        });
    });
});
