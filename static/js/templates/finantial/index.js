const markAllCheckbox = document.querySelector('[data-mark-all-checkbox]')
const checkboxes = document.querySelectorAll('input[type="checkbox"]')
const submitNavbar = document.querySelector('[data-submit-navbar]')

if(markAllCheckbox)
    markAllCheckbox.addEventListener('click', () => {
        checkboxes.forEach((checkbox) => {
            checkbox.checked = markAllCheckbox.checked
        })
    })

if(checkboxes.length)
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('click', () => {
            submitNavbar.classList.remove('hidden')
        })
    })