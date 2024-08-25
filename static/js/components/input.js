// const inputs = document.querySelectorAll(':is(input, select)')

// const toggleTouchedClass = (event) => {
//     event.target.classList.add('touched')
// }

// const initialize = (input) => {
//     input.addEventListener('blur', toggleTouchedClass)
// }

// if(inputs){
//     inputs.forEach(initialize)
// }

// FILE INPUTS

const fileInputs = document.querySelectorAll('input[type="file"]')

const toggleLabel = (event) => {
    const input = event.target
    const label = document.querySelector(`label[for="${input.id}"]`)

    if(label){
        label.textContent = input.files[0].name
    }
}

const initializeFileInputs = (input) => {
    input.addEventListener('change', toggleLabel)
}

if(fileInputs)
    fileInputs.forEach(initializeFileInputs)