const allSkills = [
    { value: "web_development", text: "Web Development" },
    { value: "graphic_design", text: "Graphic Design" },
    { value: "content_writing", text: "Content Writing" },
    { value: "digital_marketing", text: "Digital Marketing" },
    { value: "data_entry", text: "Data Entry" },
    { value: "video_editing", text: "Video Editing" },
    { value: "mobile_app_development", text: "Mobile App Development" },
    { value: "seo", text: "SEO" },
    { value: "copywriting", text: "Copywriting" },
    { value: "translation", text: "Translation" },
    { value: "social_media_management", text: "Social Media Management" },
    { value: "photography", text: "Photography" },
    { value: "virtual_assistance", text: "Virtual Assistance" },
    { value: "software_development", text: "Software Development" },
    { value: "ui_ux_design", text: "UI/UX Design" },
    { value: "project_management", text: "Project Management" },
    { value: "illustration", text: "Illustration" },
    { value: "music_production", text: "Music Production" },
    { value: "3d_modeling", text: "3D Modeling" },
    { value: "email_marketing", text: "Email Marketing" },
    { value: "copy_editing", text: "Copy Editing" },
    { value: "resume_writing", text: "Resume Writing" }
];

const searchInput = document.getElementById('searchSkills');
const skillsList = document.getElementById('skillsList');
const selectedSkillsContainer = document.getElementById('selectedSkills');
const hiddenInput = document.getElementById('selected_Skills');
let selectedSkills = [];

searchInput.addEventListener('input', function() {
    const query = this.value.toLowerCase().trim();
    skillsList.innerHTML = '';

    if (query === '') {
        return;
    }

    const filteredSkills = allSkills.filter(skill => {
        if (selectedSkills.find(s => s === skill) === undefined) {
            return skill.text.toLowerCase().includes(query);
        }
    });

    filteredSkills.forEach(skill => {
        const listItem = document.createElement('li');
        listItem.textContent = skill.text;
        listItem.style.cursor = 'pointer';
        listItem.addEventListener('click', function() {
            addSkill(skill);
            searchInput.value = '';
            skillsList.innerHTML = '';
        });
        skillsList.appendChild(listItem);
    });
});

function addSkill(skill) {
    // Check if the skill is already selected
    if (!selectedSkills.some(s => s.value === skill.value)) {
        selectedSkills.push(skill);
        updateSelectedSkills();
    }
}

function removeSkill(skill) {
    // Remove the skill from the selected skills array
    selectedSkills = selectedSkills.filter(s => s.value !== skill.value);
    updateSelectedSkills();
}

function updateSelectedSkills() {
    // Clear the current selected skills display
    selectedSkillsContainer.innerHTML = '';
    // Display all selected skills as tags
    selectedSkills.forEach(skill => {
        const skillTag = document.createElement('span');
        skillTag.textContent = skill.text + ' ×'; // '×' symbol to indicate removal
        skillTag.style.display = 'inline-block';
        skillTag.style.padding = '5px 10px';
        skillTag.style.margin = '5px 5px 0 0';
        skillTag.style.backgroundColor = '#007BFF';
        skillTag.style.color = '#fff';
        skillTag.style.borderRadius = '3px';
        skillTag.style.cursor = 'pointer';
        skillTag.addEventListener('click', function() {
            removeSkill(skill);
        });
        selectedSkillsContainer.appendChild(skillTag);
    });

    // Update the hidden input field's value
    hiddenInput.value = selectedSkills.map(skill => skill.value).join(',');
}