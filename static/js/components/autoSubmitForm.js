const forms = document.querySelectorAll('[data-auto-submit-form]')

if(forms.length)
    forms.forEach((form) => {
        const submitInput = form.querySelector('[data-auto-submit-input]')

        submitInput.addEventListener('change', () => {
            form.submit()
        })
    })