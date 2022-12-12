from js import document, console
import json
# import asyncio
from pyodide import create_proxy
from pyodide.http import pyfetch

import pandas as pd
import numpy as np
from itertools import count

def create_field(id=None):
    field = document.createElement('input')
    field.type = 'text'
    field.setAttribute('class', 'form-control-sm mb-2 row')

    if id:
        field.id = id
    return field
def create_button(textContent, id, className):

    button = document.createElement('button')
    button.type = 'button'
    button.textContent = textContent
    button.id = id
    button.setAttribute('class', className)
    return button


async def make_request(url, method, body=None, headers=None):
    
    csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

    default_headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
        'Manage': 'False'
}

    if headers:
        default_headers.update(headers)

    response = await pyfetch(
        url=url,
        method=method,
        body=body,
        headers=default_headers
)
    
    if not 200 <= response.status < 300:
        default_headers.update({'Manage': 'True'})
        response = await pyfetch(
            url=url,
            method=method,
            body=body,
            headers=default_headers
    )
        return await response.json()

    return await response.json()


def read_download_form():
    global fragment, form_loc, templateForm
    form_loc.textContent = ''
    templateForm.querySelector('#form').textContent = ''

    field_personal_id = create_field(id='id')
    field_name = create_field(id='name')
    field_last_name = create_field(id='last_name')
    field_age = create_field(id='age')
    
    field_personal_id.placeholder = 'id (* to match the rest)'
    field_name.placeholder = "name"
    field_last_name.placeholder = "last name"
    field_age.placeholder = "age"

    search = create_button('Search', 'search', 'btn btn-primary btn-sm mx-2')
    export = create_button('Export', 'export', 'btn btn-primary btn-sm mx-2')#TODO: checkear export data


    templateForm.querySelector('.card-title').textContent = 'Search and Export'
    templateForm.querySelector('#form').dataset.id = 'action-1'
    templateForm.querySelector('#form').appendChild(field_personal_id)
    templateForm.querySelector('#form').appendChild(field_name)
    templateForm.querySelector('#form').appendChild(field_last_name)
    templateForm.querySelector('#form').appendChild(field_age)
    templateForm.querySelector('#form').appendChild(search)
    templateForm.querySelector('#form').appendChild(export)
    console.log(templateForm.querySelector('#form'))

    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)
def create_form():
    global fragment, form_loc, templateForm
    form_loc.textContent = ''
    templateForm.querySelector('#form').textContent = ''

    field_personal_id = create_field(id='id')
    field_name = create_field(id='name')
    field_last_name = create_field(id='last_name')
    field_age = create_field(id='age')
    
    field_personal_id.placeholder = 'id'
    field_name.placeholder = "name"
    field_last_name.placeholder = "last name"
    field_age.placeholder = "age"

    create = create_button('Create', 'create', 'btn btn-primary btn-sm mx-2')

    templateForm.querySelector('.card-title').textContent = 'Create new profile'
    templateForm.querySelector('#form').dataset.id = 'action-2'
    templateForm.querySelector('#form').appendChild(field_personal_id)
    templateForm.querySelector('#form').appendChild(field_name)
    templateForm.querySelector('#form').appendChild(field_last_name)
    templateForm.querySelector('#form').appendChild(field_age)
    templateForm.querySelector('#form').appendChild(create)
    console.log(templateForm.querySelector('#form'))
    
    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)
def update_delete_form():
    global fragment, form_loc, templateForm
    form_loc.textContent = ''
    templateForm.querySelector('#form').textContent = ''

    field_personal_id = create_field()
    field_personal_id.placeholder = 'input exact id'

    update = create_button('Update', 'update', 'btn btn-primary btn-sm mx-2')
    delete = create_button('Delete', 'delete', 'btn btn-danger btn-sm mx-2')

    templateForm.querySelector('.card-title').textContent = 'Update or Delete profile'
    templateForm.querySelector('#form').dataset.id = 'action-3'
    templateForm.querySelector('#form').appendChild(field_personal_id)
    templateForm.querySelector('#form').appendChild(update)
    templateForm.querySelector('#form').appendChild(delete)
    console.log(templateForm.querySelector('#form'))
    
    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)

def proxy_container(e):
    global form_loc, templateForm, response_loc

    if e.target.id == 'read-download-form' or e.target.id == 'create-form' or e.target.id == 'update-delete-form':
        console.log(e.target)
        console.log(e.target.id)
        response_loc.textContent = ''

    if e.target.id == 'read-download-form':
        read_download_form()

    elif e.target.id == 'create-form':
        create_form()
        
    elif e.target.id == 'update-delete-form':
        update_delete_form()
    
    e.stopPropagation()


async def search_template():
    """
    Esta función se encarga de crear el template ante la respuesta de presionar el botón "search"
    """
    global templateSearchResponse, fragment, response_loc
    global searchResponse, searchNormalizedResponse
    
    response_loc.textContent = ''
    templateSearchResponse.querySelector('#response').textContent = ''
    templateSearchResponse.querySelector('#search-buttons').textContent = ''

    templateSearchResponse.querySelector('h5').textContent = 'Se encontraron {} resultados'.format(searchResponse['count'].values[0])
    
    console.log('Search Template')
    console.log(searchResponse.to_string())
    console.log(searchNormalizedResponse.to_string())

    templateSearchResponse.querySelector('#response').innerHTML = searchNormalizedResponse.to_html(index=True, header=False)

    if str(searchResponse['previous'].values[0]) != 'nan':
        previous = create_button(textContent='Previous Page', id='previous', className='btn btn-link btn-sm shadow m-2 p1 border border-primary')
        templateSearchResponse.querySelector('#search-buttons').appendChild(previous)
    if str(searchResponse['next'].values[0]) != 'nan':
        next = create_button(textContent='Next Page', id='next', className='btn btn-link btn-sm shadow m-2 p1 border border-primary')
        templateSearchResponse.querySelector('#search-buttons').appendChild(next)

    clone = templateSearchResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)
async def search_data(e):
    """
    Acá envía la request tomando informacion de los campos de formulario
    Atrapa los errores
    o
    Devuelve dos datasets con la respuesta de la request
    Y ejecuta la acción de renderizar la respuesta en la función "search_template"   
    """
    global searchResponse, searchNormalizedResponse, x

    x = 0

    console.log('search_data')
    
    personal_id = document.querySelectorAll('.form-control-sm')[0].value
    name = document.querySelectorAll('.form-control-sm')[1].value
    last_name = document.querySelectorAll('.form-control-sm')[2].value
    age = document.querySelectorAll('.form-control-sm')[3].value

    data = {
        'id': personal_id,
        'name': name,
        'last_name': last_name,
        'age': age
    }
    
    data = {key: value for key, value in data.items() if value != ''}
    # console.log('data', str(data))

    url = 'http://localhost:8000/api/v1/profiles/?page=1&'
    for key, value in data.items():
        url += f'{key}={value}&'
    url = url[:-1]
    # console.log(url)

    
    response = await make_request(
        url=url,
        method='GET'
    )
    # console.log(json.dumps(response))



    if response.get('errors'):
        # search for wich field is wrong
        # console.log(templateForm.querySelector('#form'))   <--- TODO: cambiar class a este elemento
        # add a classList with 'is-invalid' to the field
        # show error message
        pass
    else:
        # change classList = 'form-control form-control-sm is-valid'
        # get element of the new form-results id
        # create the needed elements to show the results
        # append the elements to the form-results


        searchResponse = pd.read_json(json.dumps(response)).loc[0, ["count", "next", "previous"]].to_frame().T
        searchNormalizedResponse = pd.json_normalize(response, record_path=['results'])
        searchNormalizedResponse.index += 1
        await search_template()

async def export_data(e):
    console.log('export_data')

    personal_id = document.querySelectorAll('.form-control-sm')[0].value
    name = document.querySelectorAll('.form-control-sm')[1].value
    last_name = document.querySelectorAll('.form-control-sm')[2].value
    age = document.querySelectorAll('.form-control-sm')[3].value

    data = {
        'id': personal_id,
        'name': name,
        'last_name': last_name,
        'age': age
    }
    data = {key: value for key, value in data.items() if value != ''}

    url = 'http://localhost:8000/api/v1/contents/?'
    for key, value in data.items():
        url += f'{key}={value}&'
    url = url[:-1]

    a = document.createElement('a')
    a.href = url
    a.download = 'export.csv'
    a.click()


async def create_data(e):
    console.log('create_data')
    # console.log('1', e.target.parentElement)

    personal_id_input = document.querySelectorAll('.form-control-sm')[0].value
    name_input = document.querySelectorAll('.form-control-sm')[1].value
    last_name_input = document.querySelectorAll('.form-control-sm')[2].value
    age_input = document.querySelectorAll('.form-control-sm')[3].value

    data = {
        'personal_id': personal_id_input,
        'name': name_input,
        'last_name': last_name_input,
        'age': age_input
    }
    
    url = 'http://localhost:8000/api/v1/profiles/'
    body = json.dumps(data)
    

    response = await make_request(
        url=url,
        method='POST',
        body=body
    )
    
    personal_id = document.getElementById('id')
    name = document.getElementById('name')
    last_name = document.getElementById('last_name')
    age = document.getElementById('age')
    
    
    if response.get('errors'):
        errors = response.get('errors')
        for field in errors.keys():
            console.log(str(field), str(errors[field]))
    else:
        console.log('request OK')

async def update_data(e):
    console.log('update_data')

    personal_id = document.querySelectorAll('.form-control-sm')[0].value

    body = json.dumps({
        'id': personal_id,
    })

    # response = await make_request(
    #     url='',
    #     method='',
    #     headers='',
    #     body=''
    # )
    console.log(body)
async def delete_data(e):
    console.log('delete_data')

    personal_id = document.querySelectorAll('.form-control-sm')[0].value

    body = json.dumps({
        'id': personal_id,
    })

    # response = await make_request(
    #     url='',
    #     method='',
    #     headers='',
    #     body=''
    # )
    console.log(body)

async def proxy_form_location(e):
    global templateForm

    action = templateForm.querySelector('#form').dataset.id
    button_id = e.target.id

    if action == 'action-1' and button_id == 'search':
        console.log(e.target)
        data = await search_data(e)

    elif action == 'action-1' and button_id == 'export':
        console.log(e.target)
        data = await export_data(e)

    elif action == 'action-2' and button_id == 'create':
        console.log(e.target)
        data = await create_data(e)

    elif action == 'action-3' and button_id == 'update':
        console.log(e.target)
        data = await update_data(e)

    elif action == 'action-3' and button_id == 'delete':
        console.log(e.target)
        data = await delete_data(e)

    e.stopPropagation()


async def change_page(e, forward):
    """
    Esta función se encarga de hacer el request con la nueva página
    """
    global searchResponse, searchNormalizedResponse, x
    console.log('change_page')
    
    if forward:
        console.log('forward')
        response = await make_request(
        url=searchResponse['next'][0],
        method='GET'
    )

    else:
        console.log('back')
        response = await make_request(
        url=searchResponse['previous'][0],
        method='GET'
    )
    console.log(json.dumps(response))

    searchResponse = pd.read_json(json.dumps(response)).loc[0, ["count", "next", "previous"]].to_frame().T
    searchNormalizedResponse = pd.json_normalize(response, record_path=['results'])
    searchNormalizedResponse.index += 1
    if forward:
        x += 1
        searchNormalizedResponse.index += (5 * x)
    else:
        x -= 1
        searchNormalizedResponse.index += (5 * x)

    await search_template()

async def proxy_response_location(e):
    global templateSearchResponse, response_loc

    if e.target.id == 'previous' or e.target.id == 'next':
        console.log(e.target)
        # response_loc.textContent = ''

    if e.target.id == 'previous':
        console.log('previous')
        data = await change_page(e, forward=False)

    elif e.target.id == 'next':
        console.log('next')
        data = await change_page(e, forward=True)

def main():
    # created in HTML
    global container, templateForm, form_loc
    global templateSearchResponse, response_loc

    # created localy
    global fragment, searchResponse, searchNormalizedResponse, x

    x = 0
    fragment = document.createDocumentFragment()
    searchResponse = pd.DataFrame()
    searchNormalizedResponse = pd.DataFrame()

    container = document.querySelector('.container')
    form_loc = document.querySelector('#form-loc')
    response_loc = document.querySelector('#response-loc')
    templateForm = document.getElementById('template-form').content
    templateSearchResponse = document.getElementById('template-search-response').content
    

    container.addEventListener('click', create_proxy(proxy_container))

    form_loc.addEventListener('click', create_proxy(proxy_form_location))

    response_loc.addEventListener('click', create_proxy(proxy_response_location))


main()