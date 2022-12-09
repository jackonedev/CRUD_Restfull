from js import document, console
import json
from pyodide.http import pyfetch
from pyodide import create_proxy


async def make_request(url, method, body=None, headers=None):
    default_headers = {
        'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
}

    if headers:
        default_headers.update(headers)

    response = await pyfetch(
        url=url,
        method=method,
        body=body,
        headers=default_headers
)
    return await response.json()


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


def read_download():
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


def create():
    global fragment, form_loc, templateForm
    form_loc.textContent = ''
    templateForm.querySelector('#form').textContent = ''

    field_personal_id = create_field()
    field_personal_id.placeholder = 'input exact id'

    create = create_button('Create', 'create', 'btn btn-primary btn-sm mx-2')

    templateForm.querySelector('.card-title').textContent = 'Create new profile'
    templateForm.querySelector('#form').dataset.id = 'action-2'
    templateForm.querySelector('#form').appendChild(field_personal_id)
    templateForm.querySelector('#form').appendChild(create)
    console.log(templateForm.querySelector('#form'))
    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)
    


def update_delete():
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

    if e.target.id == 'read-download':
        console.log(e.target.id)
        read_download()

    elif e.target.id == 'create':
        console.log(e.target.id)
        create()
    elif e.target.id == 'update-delete':
        console.log(e.target.id)
        update_delete()
    
    e.stopPropagation()

    console.log('proxy_container')


def search_data(e):
    console.log('search_data')
    search = templateForm.querySelector('#search')
    

def export_data(e):
    console.log('export_data')
    export = templateForm.querySelector('#export')
    pass
def create_data(e):
    create = templateForm.querySelector('#create')
    console.log('create_data')
    pass
def update_data(e):
    console.log('update_data')
    update = templateForm.querySelector('#update')
    pass
def delete_data(e):
    console.log('delete_data')
    delete = templateForm.querySelector('#delete')
    pass

def proxy_form_location(e):
    global form_loc, templateForm
    console.log('hola')

    action = templateForm.querySelector('#form').dataset.id
    button_id = e.target.id

    if action == 'action-1' and button_id == 'search':
        search_data(e)

    elif action == 'action-1' and button_id == 'export':
        export_data(e)

    elif action == 'action-2' and button_id == 'create':
        create_data(e)

    elif action == 'action-3' and button_id == 'update':
        update_data(e)

    elif action == 'action-3' and button_id == 'delete':
        delete_data(e)

    e.stopPropagation()

def main():
    global container, templateForm, form_loc
    global fragment
    fragment = document.createDocumentFragment()

    container = document.querySelector('.container')
    form_loc = document.querySelector('#form-loc')
    btn_loc = document.querySelector('#btn-loc')
    templateForm = document.getElementById('template-form').content
    


    container.addEventListener('click', create_proxy(proxy_container))

    form_loc.addEventListener('click', create_proxy(proxy_form_location))


main()