const monthInput = document.querySelector('[data-month-input]')
const form = monthInput.parentElement

monthInput.addEventListener('change', () => {
    form.submit()
})