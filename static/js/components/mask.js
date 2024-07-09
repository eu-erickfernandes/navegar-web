const mask = {
    date (event){
        const field = event.target
        field.maxLength = '10'
        const value = field.value

        const newValue = value
        .replace(/\D/g, '')
        .replace(/(\d{2})(\d)/, '$1/$2')
        .replace(/(\d{2})(\d)/, '$1/$2')

        field.value = newValue
    }
}

const initMaskFields = () => {
    const fields = document.querySelectorAll('[data-mask]')

    fields.forEach((field) => {
        const method = field.getAttribute('data-mask')

        field.addEventListener('input', mask[method])
        field.dispatchEvent(new Event('input'))
    })
}

initMaskFields()