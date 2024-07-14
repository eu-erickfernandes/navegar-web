const inputs = document.querySelectorAll(':is(input, select)')

const toogleTouchedClass = (event) => {
    event.target.classList.add('touched')
}

const initialize = (input) => {
    input.addEventListener('blur', toogleTouchedClass)

    if(input.type == 'file')
        input.addEventListener('change', toogleTouchedClass)
}

if(inputs){
    inputs.forEach(initialize)
}