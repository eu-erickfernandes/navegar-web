const form = document.querySelector('form')
const initialBoatCard = document.querySelector('[data-boat-card]')
const addButton = document.querySelector('[data-add-button]')

const enumerateBoats = () => {
    const newBoatCards = document.querySelectorAll('[data-boat-card="new"]')

    newBoatCards.forEach((boatCard, index) => {
        const select = boatCard.querySelector('select')
        select.id = `boat-${index}`
        select.name = `boat-${index}`

        const checkboxes = boatCard.querySelectorAll('input')
        
        checkboxes.forEach((checkbox) => {
            const name = checkbox.name
            const weekday = name.split('-')
            const newName = `${index}-weekday-${weekday[weekday.length - 1]}`
            
            const label = boatCard.querySelector(`label[for="${name}"]`) 
            label.setAttribute('for', newName)
            
            checkbox.name = newName
            checkbox.id = newName
        })
    })
}

enumerateBoats()

const removeCurrentBoat = (event) => {
    const removeSpan = event.target
    const card = removeSpan.parentElement.parentElement

    card.remove()
}

const initializingRemoveBoat = () => {
    const removeSpans = document.querySelectorAll('[data-boat-remove]')

    removeSpans.forEach((span) => {
        span.addEventListener('click', removeCurrentBoat)
    })
}

initializingRemoveBoat()

const addBoat = () => {
    const newBoatCard = initialBoatCard.cloneNode(true)
    newBoatCard.setAttribute('data-boat-card', 'new')

    const select = newBoatCard.querySelector('select')
    select.value = ''
    
    const checkboxes = newBoatCard.querySelectorAll('input')
    
    checkboxes.forEach((checkbox) => {
        checkbox.checked = false
    })

    form.insertBefore(newBoatCard, addButton)

    enumerateBoats()
    initializingRemoveBoat()
}

addButton.addEventListener('click', addBoat)