const radioControls = document.querySelectorAll('[data-radio-control]')
const targets = document.querySelectorAll('[data-radio-control-target]')

console.log(radioControls, targets)

// INTIALIZAING THE COMPONENTS

if(radioControls.length){
    const showTarget = () => {
        const radioChecked = [...radioControls].filter(target => target.checked).at(0)
    
        const radioKey = radioChecked.getAttribute('data-radio-control')

        console.log(radioChecked, radioKey)
        
        targets.forEach((target) => {
            const targetKey = target.getAttribute('data-radio-control-target')

            console.log(targetKey)
    
            if(targetKey == radioKey){
                target.classList.remove('hidden')
            }else{
                target.classList.add('hidden')
                target.value = ''
            }
        })
    } 

    radioControls.forEach((radio) => {
        radio.addEventListener('click', showTarget)
    })
    
    showTarget()
}