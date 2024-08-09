const roleRadios = document.querySelectorAll('[data-role-radio]')
const uploadTicketControl = document.querySelector('[data-upload-ticket-control]')

const manageUploadTicketControl = () => {
    uploadTicketControl.classList.add('hidden')

    roleRadios.forEach((radio) => {
        if(radio.checked && radio.value == 'S')
            uploadTicketControl.classList.remove('hidden')
    })
}

manageUploadTicketControl()

roleRadios.forEach((radio) => {
    radio.addEventListener('click', manageUploadTicketControl)
})