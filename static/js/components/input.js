// const inputs = document.querySelectorAll(':is(input, select)')

// const toogleTouchedClass = (event) => {
//     event.target.classList.add('touched')
// }

// const initialize = (input) => {
//     input.addEventListener('blur', toogleTouchedClass)
// }

// if(inputs){
//     inputs.forEach(initialize)
// }

// FILE INPUTS

const fileInputs = document.querySelectorAll('input[type="file"]')

const toogleLabel = (event) => {
    const input = event.target
    const label = document.querySelector(`label[for="${input.id}"]`)

    if(label){
        label.textContent = input.files[0].name
    }
}

const initializeFileInputs = (input) => {
    input.addEventListener('change', toogleLabel)
}

if(fileInputs)
    fileInputs.forEach(initializeFileInputs)