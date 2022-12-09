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
    
def create_field():
    field = document.createElement('input')
    field.type = 'text'
    field.setAttribute('class', 'form-control-sm mb-2 row')
    return field


def read_download():
    global fragment, form_loc, templateForm

    field_personal_id = create_field()
    field_name = create_field()
    field_last_name = create_field()
    field_age = create_field()
    
    field_personal_id.placeholder = 'id (* to match the rest)'
    field_name.placeholder = "name"
    field_last_name.placeholder = "last name"
    field_age.placeholder = "age"

    
    # field_personal_id.className += 'col-xs-4'
    # field_personal_id.className += 'border border-primary'

    templateForm.querySelector('.card-title').textContent = 'Search and Export'
    templateForm.querySelector('#form').appendChild(field_personal_id)
    templateForm.querySelector('#form').appendChild(field_name)
    templateForm.querySelector('#form').appendChild(field_last_name)
    templateForm.querySelector('#form').appendChild(field_age)
    console.log(templateForm.querySelector('#form'))

    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)

    form_loc.appendChild(fragment)


def create():
    global fragment, form_loc, templateForm
    field_personal_id = create_field()
    field_personal_id.placeholder = 'input exact id'

    templateForm.querySelector('.card-title').textContent = 'Create new profile'
    templateForm.querySelector('#form').appendChild(field_personal_id)
    console.log(templateForm.querySelector('#form'))
    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)


def update_delete():
    global fragment, form_loc, templateForm
    field_personal_id = create_field()
    field_personal_id.placeholder = 'input exact id'

    templateForm.querySelector('.card-title').textContent = 'Update or Delete profile'
    templateForm.querySelector('#form').appendChild(field_personal_id)
    console.log(templateForm.querySelector('#form'))
    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)

def proxy_container(e):
    global form_loc, templateForm
    console.log(e.target)

    form_loc.textContent = ''
    templateForm.querySelector('#form').textContent = ''

    if e.target.id == 'read-download':
        console.log(e.target.id)
        read_download()
    elif e.target.id == 'create':
        console.log(e.target.id)
        create()
    elif e.target.id == 'update-delete':
        console.log(e.target.id)
        update_delete()



def main():
    global templateForm, form_loc, templateButtons, container
    global fragment

    container = document.querySelector('.container')
    form_loc = document.querySelector('#form-loc')
    templateForm = document.getElementById('template-form').content
    fragment = document.createDocumentFragment()


    container.addEventListener('click', create_proxy(proxy_container))




main()