const finantialSheet = document.querySelector('[data-finantial-sheet]')
const markAllCheckbox = document.querySelector('[data-mark-all-checkbox]')
const checkboxes = document.querySelectorAll('input[type="checkbox"]')

if(markAllCheckbox)
    markAllCheckbox.addEventListener('click', () => {
        checkboxes.forEach((checkbox) => {
            checkbox.checked = markAllCheckbox.checked
        })
    })

if(finantialSheet)
    finantialSheet.querySelectorAll('tbody tr').forEach((tr) => {
        tr.addEventListener('click', (event) => {
            if(event.target.tagName != 'INPUT' && !event.target.classList.contains('editable-data')){
                const checkbox = tr.querySelector('input[type="checkbox"]')
                checkbox.checked = !checkbox.checked
            }
        })
    })