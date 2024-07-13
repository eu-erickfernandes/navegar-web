const mask = {
    cpf(event){
        const field = event.target
        field.maxLength = '14'
        const value = field.value

        const newValue = value
        .replace(/\D/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1-$2')

        field.value = newValue
    },

    current(event){
        const field = event.target
        field.maxLength = '23'
        const valor = field.value

        const options = {style: 'currency', currency: 'BRL'}

        const newValue = valor
        .replace(/\D/g, '')

        const formatedValue = new Intl.NumberFormat('pt-br', options).format(newValue / 100)

        field.value = formatedValue
    },

    date (event){
        const field = event.target
        field.maxLength = '10'
        const value = field.value

        const newValue = value
        .replace(/\D/g, '')
        .replace(/(\d{2})(\d)/, '$1/$2')
        .replace(/(\d{2})(\d)/, '$1/$2')

        field.value = newValue
    },

    phone(event){
        const field = event.target
        field.maxLength = '15'
        const value = field.value

        const newValue = value
        .replace(/\D/g, '')
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(\d)(\d{3})-(\d)(\d{3})(\d)/, '$1 $2$3-$4$5')

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