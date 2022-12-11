from js import document, console
import json
# import asyncio
from pyodide.http import pyfetch
from pyodide import create_proxy

import pandas as pd

def create_field(id=None):
    field = document.createElement('input')
    field.type = 'text'
    field.setAttribute('class', 'form-control-sm mb-2 row')

    if id:
        field.id = id
    return field
def create_button(textContent, id, class_name):

    button = document.createElement('button')
    button.type = 'button'
    button.textContent = textContent
    button.id = id
    button.setAttribute('class', class_name)
    return button

async def make_request(url, method, body=None, headers=None):
    
    csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

    default_headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
}

    if method != 'GET':
        default_headers.update({
            'X-CSRFToken': csrf
})

    if headers:
        default_headers.update(headers)

    response = await pyfetch(
        url=url,
        method=method,
        body=body,
        headers=default_headers
)
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
    export = create_button('Export', 'export', 'btn btn-primary btn-sm mx-2')
    
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
    global form_loc, templateForm
    console.log(e.target)

    if e.target.id == 'read-download-form':
        console.log(e.target.id)
        read_download_form()

    elif e.target.id == 'create-form':
        console.log(e.target.id)
        create_form()
    elif e.target.id == 'update-delete-form':
        console.log(e.target.id)
        update_delete_form()
    
    e.stopPropagation()


def search_template():
    global templateSearchResponse, fragment, response_loc
    global searchResponse, searchNormalizedResponse
    templateSearchResponse.querySelector('h5').textContent = 'Hola mundo tranqui!'
    
    console.log('ESTOY EN SEARCH TEMPLATE')
    console.log(str(searchResponse.to_dict))
    console.log(str(searchNormalizedResponse.to_dict))
    clone = templateSearchResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)

async def search_data(e):
    global searchResponse, searchNormalizedResponse

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
    console.log('data', str(data))

    url = 'http://localhost:8000/api/v1/profiles/?page=1&'
    for key, value in data.items():
        url += f'{key}={value}&'
    url = url[:-1]
    # console.log(url)

    
    response = await make_request(
        url=url,
        method='GET'
    )
    console.log(json.dumps(response))


    # console.log(json.dumps(response['count']))


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


        searchResponse = pd.read_json(json.dumps(response)).loc[0, ["count", "next", "previous"]]
        # searchNormalizedResponse = pd.json_normalize(json.dumps(response), record_path=['results'])
        searchNormalizedResponse = pd.json_normalize(response, record_path=['results'])
        search_template()



async def export_data(e):
    console.log('export_data')

    personal_id = document.querySelectorAll('.form-control-sm')[0].value
    name = document.querySelectorAll('.form-control-sm')[1].value
    last_name = document.querySelectorAll('.form-control-sm')[2].value
    age = document.querySelectorAll('.form-control-sm')[3].value

    body = json.dumps({
        'id': personal_id,
        'name': name,
        'last_name': last_name,
        'age': age
    })

    # response = await make_request(
    #     url='',
    #     method='',
    #     headers='',
    #     body=''
    # )
    console.log(body)
async def create_data(e):
    console.log('create_data')
    # console.log('1', e.target.parentElement)

    personal_id = document.querySelectorAll('.form-control-sm')[0].value
    name = document.querySelectorAll('.form-control-sm')[1].value
    last_name = document.querySelectorAll('.form-control-sm')[2].value
    age = document.querySelectorAll('.form-control-sm')[3].value

    body = json.dumps({
        'id': personal_id,
        'name': name,
        'last_name': last_name,
        'age': age
    })
    
    # response = await make_request(
    #     url='api/v1/profiles/',
    #     method='GET',
    #     headers='',
    #     body=''
    # )
    console.log(body)
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
    global form_loc, templateForm

    action = templateForm.querySelector('#form').dataset.id
    button_id = e.target.id

    if action == 'action-1' and button_id == 'search':
        data = await search_data(e)

    elif action == 'action-1' and button_id == 'export':
        data = await export_data(e)

    elif action == 'action-2' and button_id == 'create':
        data = await create_data(e)

    elif action == 'action-3' and button_id == 'update':
        data = await update_data(e)

    elif action == 'action-3' and button_id == 'delete':
        data = await delete_data(e)

    e.stopPropagation()


async def proxy_result_location(e):
    console.log('proxy_result_location')

def main():
    # created in HTML
    global container, templateForm, form_loc
    global templateSearchResponse, response_loc

    # created localy
    global fragment, searchResponse, searchNormalizedResponse

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

    response_loc.addEventListener('click', create_proxy(proxy_result_location))


main()