const forms = document.querySelectorAll('[data-auto-submit-form]')

if(forms.length)
    forms.forEach((form) => {
        const submitInputs = form.querySelectorAll('[data-auto-submit-input]')

        submitInputs.forEach((submitInput) => {

            submitInput.addEventListener('change', () => {
                form.submit()
            })
        })
    })