const rebookingCheckbox = document.querySelector('[data-rebooking-checkbox]')
const noShowCheckbox = document.querySelector('[data-no-show-checkbox]')

const radioPassenger = document.querySelector('[data-radio-passenger]')
const radioCargo = document.querySelector('[data-radio-cargo]')

const groupPassenger = document.querySelector('[data-group-passenger]')
const groupCargo = document.querySelector('[data-group-cargo]')

const quantityInput = document.querySelector('[data-quantity-input]')
const quantityAdd = document.querySelector('[data-quantity-add]')
const quantityRemove = document.querySelector('[data-quantity-remove]')

rebookingCheckbox.addEventListener('click', () => {
    if(rebookingCheckbox.checked)
        noShowCheckbox.checked = false
})

noShowCheckbox.addEventListener('click', () => {
    if(noShowCheckbox.checked)
        rebookingCheckbox.checked = false
})

// TICKET TYPE CONTROL
const switchType = () => {
    // SHOWING THE CORRECT GROUP 
    if(radioPassenger.checked){
        groupPassenger.classList.remove('hidden')
        groupCargo.classList.add('hidden')
    }else{
        groupPassenger.classList.add('hidden')
        groupCargo.classList.remove('hidden')
    }

    // CONTROLLING THE PASSENGER GROUP INPUTS
    groupPassenger.querySelectorAll('input').forEach((input) => input.disabled = radioCargo.checked)

    // CONTROLLING THE CARGO GROUP INPUTS
    groupCargo.querySelectorAll('input').forEach((input) => input.disabled = radioPassenger.checked)
}

switchType()

radioPassenger.addEventListener('click', switchType)
radioCargo.addEventListener('click', switchType)

// REMOVE A SELECTED PASSENGER
const removeCurrentPassenger = (event) => {
    const removeSpan = event.currentTarget
    const dropdown = removeSpan.parentElement.parentElement 

    const radioChecked = dropdown.querySelector('input:checked')

    if(radioChecked){
        radioChecked.checked = false

        // ENABLING THE TEXT INPUTS
        dropdown.querySelectorAll('input[type="text"]').forEach((input) => {
            input.disabled = false
        })
    }else{
        dropdown.remove()
        updateQuantity()
        enumeratePassengers()
    }
}

// ENUMERATING INPUT NAMES AND IDS
const enumeratePassengers = () => {
    const passengersDropdowns = document.querySelectorAll('[data-passenger-dropdown]')

    passengersDropdowns.forEach((dropdown, index) => {
        const summary = dropdown.querySelector('summary')
        summary.textContent = `Passageiro ${index+1}`

        const nameInput = dropdown.querySelector('[data-passenger-name]')
        nameInput.name = `passenger_name_${index}`
        
        const birthInput = dropdown.querySelector('[data-passenger-birth]')
        birthInput.name = `passenger_birth_${index}`

        const radioInputs = dropdown.querySelectorAll('input[type="radio"]')
        radioInputs.forEach((radio) => {
            radio.id = `${radio.id}-${index}`
            radio.name = `radio_passenger_${index}`
        })

        const radioLabels = dropdown.querySelectorAll('label')
        radioLabels.forEach((label) => {
            const labelFor = label.getAttribute('for')
            label.setAttribute('for', `${labelFor}-${index}`)
        })

        const cpfInput = dropdown.querySelector('[data-passenger-cpf]')
        cpfInput.name = `passenger_cpf_${index}`
        
        const rgInput = dropdown.querySelector('[data-passenger-rg]')
        rgInput.name = `passenger_rg_${index}`

        const removeSpan = dropdown.querySelector('[data-passenger-remove]')

        removeSpan.addEventListener('click', removeCurrentPassenger)
    })
}

enumeratePassengers()

const namingDropdowns = () => {
    const passengersDropdowns = document.querySelectorAll('[data-passenger-dropdown]')

    passengersDropdowns.forEach((dropdown, index) => {
        // const summary = dropdown.querySelector('summary')
        // summary.textContent = `Passageiro ${index+1}`
        const checkedRadio = dropdown.querySelector('input:checked')
        const nameInput = dropdown.querySelector('[data-passenger-name]')
        const summary = dropdown.querySelector('summary')

        if(checkedRadio){
            const id = checkedRadio.id
            const label = dropdown.querySelector(`label[for="${id}"]`)

            summary.textContent = label.querySelector('span').textContent
        }else if(nameInput.value){
            summary.textContent = nameInput.value
        }else{
            summary.textContent = `Passageiro ${index+1}`
        }
    })
}

// HANDLE THE CLOSING DROPDOWN
const handleClose = (event) => {
    dropdown = event.target

    if(!dropdown.open){
        const checkedRadio = dropdown.querySelector('input:checked')
        const nameInput = dropdown.querySelector('[data-passenger-name]')

        if(checkedRadio || nameInput.value)
            dropdown.classList.add('selected')
        else
            dropdown.classList.remove('selected')

        // if(checkedRadio){
        //     const id = checkedRadio.id
        //     const label = dropdown.querySelector(`label[for="${id}"]`)

        //     summary.textContent = label.querySelector('span').textContent
        // }else if(nameInput.value){
        //     summary.textContent = nameInput.value
        // }
    }

    namingDropdowns()
}

const initializingDropdowns = () => {
    document.querySelectorAll('[data-passenger-dropdown]').forEach((dropdown) => {
        dropdown.addEventListener('toggle', handleClose)
    })
}

initializingDropdowns()

// HANDLING SEARCH INPUT
const handlePassengerSearch = (event) => {
    const input = event.target
    const value = input.value

    const passengersList = input.parentElement.querySelector('[data-passenger-list]')
    
    passengersList.querySelectorAll('label').forEach((label) => {
        if(label.textContent.toUpperCase().includes(value.toUpperCase()))
            label.parentElement.classList.remove('hidden')
        else
            label.parentElement.classList.add('hidden')
    })
}

const initializingSearchInputs = () => {
    document.querySelectorAll('[data-passenger-name]').forEach((input) => {
        input.addEventListener('input', handlePassengerSearch)
    })
}

initializingSearchInputs()

// HANDLING THE PASSENGER SELECTION INSIDE THE LIST
const handlePassengerSelect = (event) => {
    const radio = event.target
    
    const passengerForm = radio
    .parentElement
    .parentElement
    .parentElement
    .parentElement

    // CLEANING AND DISABLING THE TEXT INPUTS
    passengerForm.querySelectorAll('input[type="text"]').forEach((input) => {
        input.value = ''
        input.disabled = true
    })

    const dropdown = passengerForm.parentElement
    dropdown.toggleAttribute('open')
}

const initializingPassengersRadios = () => {
    document.querySelectorAll('[data-passenger-dropdown] input[type="radio"]').forEach((radio) => {
        radio.addEventListener('click', handlePassengerSelect)
    })
}

initializingPassengersRadios()

// UPDATE THE PASSENGER QUANTITY INPUT VALUE
const updateQuantity = () => {
    quantityInput.value = document.querySelectorAll('[data-passenger-dropdown]').length
}

// ADD PASSENGER DROPDOWN
const addPassenger = () => {
    const dropdown = document.querySelector('[data-passenger-dropdown]')
    const html = dropdown.innerHTML

    const newDropdown = document.createElement('details')
    newDropdown.classList.add('passenger-dropdown')
    newDropdown.setAttribute('data-passenger-dropdown', '')
    newDropdown.innerHTML = html
    newDropdown.name = 'passenger'

    newDropdown.querySelectorAll('input').forEach((input) => input.disabled = false)

    groupPassenger.appendChild(newDropdown)
    enumeratePassengers()
    namingDropdowns()
    updateQuantity()
    initMaskFields()
    initializingDropdowns()
    initializingPassengersRadios()
    initializingSearchInputs()
}

quantityAdd.addEventListener('click', addPassenger)

// REMOVE PASSENGER VIA QUANTITY CONTROL
const removePassenger = () => {
    const passengersDropdowns = document.querySelectorAll('[data-passenger-dropdown]')
    const length = passengersDropdowns.length

    if(length > 1)
        passengersDropdowns[length-1].remove()

    enumeratePassengers()
    namingDropdowns()
    updateQuantity()
}

quantityRemove.addEventListener('click', removePassenger)