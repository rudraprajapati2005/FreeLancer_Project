document.addEventListener("DOMContentLoaded", function () {
    function animateCountUp(element, target, duration) {
        let start = 0;
        let increment = target / (duration / 10); // Adjust speed
        let interval = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target;
                clearInterval(interval);
            } else {
                element.textContent = Math.floor(start);
            }
        }, 10);
    }

    // Start animations when the page loads
    animateCountUp(document.getElementById("clients-count"), 100, 2000);
    animateCountUp(document.getElementById("freelancers-count"), 350, 2500);
    animateCountUp(document.getElementById("projects-count"), 150, 2200);
});
