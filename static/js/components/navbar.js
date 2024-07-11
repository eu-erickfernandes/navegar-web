const current_path = window.location.pathname.split('/')
const links = document.querySelectorAll('[data-navbar-link]')

console.log(current_path)

if(links)
    if (current_path.length == 2)
        document.querySelectorAll(('[data-navbar-link="/"]')).forEach((link) => {
            link.classList.add('active')
        })
    else
        links.forEach((link) => {
            const paths = link.getAttribute('data-navbar-link').split(' ')

            paths.forEach((path) => {
                if (current_path.includes(path))
                    link.classList.add('active')
            })
        })