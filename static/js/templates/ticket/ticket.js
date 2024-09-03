const noShowCheckbox = document.querySelector('[data-no-show-checkbox]')

if (noShowCheckbox){
    const priceInput = document.querySelector('[data-price-input]')
    const originalPrice = priceInput.getAttribute('data-price-input')

    const handleCheck = () => {
        const newPrice = noShowCheckbox.checked ? (Number.parseFloat(originalPrice) * 0.30).toFixed(2) : originalPrice
        priceInput.value = newPrice
    }

    noShowCheckbox.addEventListener('click', handleCheck)
}