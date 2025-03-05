import  { allSkills } from './skills.js';

let selectedSkills = []; // Store selected skills

document.addEventListener("DOMContentLoaded", function () {
    const skillSearchInput = document.getElementById("skill-search");
    const skillList = document.getElementById("skill-list");
    const selectedSkillsContainer = document.getElementById("selected-skills");
    const applyFiltersBtn = document.getElementById("apply-filters");
    const projectSearchInput = document.getElementById("project-search");
    const projectCards = document.querySelectorAll(".project-card");
    console.log(allSkills)
    // Dummy list of skills (In real scenario, fetch from backend)
    
    // Filter skills dynamically as user types
    skillSearchInput.addEventListener("input", function () {
        const query = skillSearchInput.value.toLowerCase();
        skillList.innerHTML = ""; // Clear previous list

        if (query) {
            const filteredSkills = allSkills.filter(skill => skill.toLowerCase().includes(query));
            filteredSkills.forEach(skill => {
                const li = document.createElement("li");
                li.textContent = skill;
                li.addEventListener("click", function () {
                    addSkill(skill);
                });
                skillList.appendChild(li);
            });
        }
    });

    // Function to add a selected skill
    function addSkill(skill) {
        if (!selectedSkills.includes(skill)) {
            selectedSkills.push(skill);
            updateSelectedSkills();
        }
        skillSearchInput.value = ""; // Clear input after selection
        skillList.innerHTML = ""; // Clear suggestion list
    }

    // Function to remove skill and update projects dynamically
    function removeSkill(skill) {
        selectedSkills = selectedSkills.filter(s => s !== skill);
        updateSelectedSkills();
        filterProjects(); // Reapply filtering
    }

    // Function to update selected skills display
    function updateSelectedSkills() {
        selectedSkillsContainer.innerHTML = "";
        selectedSkills.forEach(skill => {
            const skillTag = document.createElement("span");
            skillTag.classList.add("skill-tag");
            skillTag.textContent = skill;
            skillTag.addEventListener("click", function () {
                removeSkill(skill);
            });
            selectedSkillsContainer.appendChild(skillTag);
        });
    }

    // Function to filter projects based on selected skills
    function filterProjects() {
        projectCards.forEach(card => {
            const skillsText = card.querySelector(".skills").textContent.toLowerCase();
            const hasAllSkills = selectedSkills.every(skill => skillsText.includes(skill.toLowerCase()));

            if (selectedSkills.length === 0 || hasAllSkills) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }

    // Apply filters when button is clicked
    applyFiltersBtn.addEventListener("click", filterProjects);

    // Search projects by name
    projectSearchInput.addEventListener("input", function () {
        const query = projectSearchInput.value.toLowerCase();
        projectCards.forEach(card => {
            const title = card.querySelector("h2").textContent.toLowerCase();
            if (title.includes(query)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
