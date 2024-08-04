const routeSearch = document.querySelector('[data-route-search]')
const routeItems = document.querySelectorAll('[data-route-item]')

const searchRoute = () => {
    const value = routeSearch.value

    routeItems.forEach((item) => {
        const route = item.getAttribute('data-route-item')

        if (route.toUpperCase().includes(value.toUpperCase()))
            item.classList.remove('hidden')
        else
            item.classList.add('hidden')
    })
}

routeSearch.addEventListener('input', searchRoute)