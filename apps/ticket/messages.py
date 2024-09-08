from utils.format import date_format

from services.whatsapp_api import send_message

def ticket_creation_message(request, ticket):
    date = f'{str(ticket.date).split("-")[2]}/{str(ticket.date).split("-")[1]}/{str(ticket.date).split("-")[0]}'
    pdf_path = f'http://{request.get_host()}/passagens/{ticket.id}/pdf'
    
    description = ''

    if ticket.passenger:
        description = f'*{ticket.passenger.name}*\n'

        description += f'CPF: {ticket.passenger.cpf}\n' if ticket.passenger.cpf else ''

        description += f'RG: {ticket.passenger.rg}\n' if ticket.passenger.rg else ''

        description += f'Nascimento: {ticket.passenger.birth_date}' if ticket.passenger.birth_date else ''

    if ticket.cargo:
        description = f'Carga: {ticket.cargo.description}'

        description += f'\nPeso: {ticket.cargo.weight}' if ticket.cargo.weight else ''

    message = f'*{date} {ticket.origin} - {ticket.destination}*\n'
    message += f'```Cód: {ticket.id}```\n'
    
    message += f'Saída: {ticket.departure_time}\nChegada: {ticket.arrival_time}\n'

    message += f'Lancha: {ticket.boat}\nValor: {ticket.price}\n'

    message += f'{description}'

    if not ticket.boat.supplier.upload_ticket and ticket.status == 'pending':
        message += f'\n\n*VOUCHER*\n{pdf_path}'

    send_message('ADM', message)

    if ticket.status == 'pending':
        send_message(ticket.boat.supplier.whatsapp_phone, message)


def ticket_rebooking_message(request, ticket):
    date = f'{str(ticket.date).split("-")[2]}/{str(ticket.date).split("-")[1]}/{str(ticket.date).split("-")[0]}'
    pdf_path = f'http://{request.get_host()}/passagens/{ticket.id}/pdf/'
    
    description = ''

    if ticket.passenger:
        description = f'*{ticket.passenger.name}*\n'

        description += f'CPF: {ticket.passenger.cpf}\n' if ticket.passenger.cpf else ''

        description += f'RG: {ticket.passenger.rg}\n' if ticket.passenger.rg else ''

        description += f'Nascimento: {ticket.passenger.birth_date}' if ticket.passenger.birth_date else ''

    if ticket.cargo:
        description = f'Carga: {ticket.cargo.description}'

        description += f'\nPeso: {ticket.cargo.weight}' if ticket.cargo.weight else ''

    message = f'*_REMARCAÇÂO_*\n'
    message += f'```Cód: {ticket.id}```\n'

    message += f'*{date} {ticket.origin} - {ticket.destination}*\n'
    
    message += f'Saída: {ticket.departure_time}\nChegada: {ticket.arrival_time}\n'

    message += f'Lancha: {ticket.boat}\nValor: {ticket.price}\n'

    message += f'{description}'

    if not ticket.boat.supplier.upload_ticket and ticket.status == 'pending':
        message += f'\n\n*VOUCHER*\n{pdf_path}'

    send_message('ADM', message)

    if ticket.status == 'pending':
        send_message(ticket.boat.supplier.whatsapp_phone, message)


def ticket_no_show_message(request, ticket):
    date = f'{str(ticket.date).split("-")[2]}/{str(ticket.date).split("-")[1]}/{str(ticket.date).split("-")[0]}'
    
    description = ''

    if ticket.passenger:
        description = f'*{ticket.passenger.name}*\n'

        description += f'CPF: {ticket.passenger.cpf}\n' if ticket.passenger.cpf else ''

        description += f'RG: {ticket.passenger.rg}\n' if ticket.passenger.rg else ''

        description += f'Nascimento: {ticket.passenger.birth_date}' if ticket.passenger.birth_date else ''

    if ticket.cargo:
        description = f'Carga: {ticket.cargo.description}'

        description += f'\nPeso: {ticket.cargo.weight}' if ticket.cargo.weight else ''

    message = f'*_NO-SHOW_*\n'
    message += f'```Cód: {ticket.id}```\n'

    message += f'*{date} {ticket.origin} - {ticket.destination}*\n'
    
    message += f'Saída: {ticket.departure_time}\nChegada: {ticket.arrival_time}\n'

    message += f'Lancha: {ticket.boat}\nValor: {ticket.price}\n'

    message += f'{description}'

    send_message('ADM', message)

    if ticket.status == 'pending':
        send_message(ticket.boat.supplier.whatsapp_phone, message)


def additional_creation_message(request, additional):
    message = f'*_ADICIONAL_*\n'

    message += f'```Cód. da Passagem: #{additional.ticket.id}```\n\n'

    message += f'*Descrição:* {additional.description}\n'
    message += f'*Valor:* {additional.value}'

    send_message('ADM', message)