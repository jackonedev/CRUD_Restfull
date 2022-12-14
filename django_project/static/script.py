from js import document, console
import json

# import asyncio
from pyodide import create_proxy
from pyodide.http import pyfetch

import pandas as pd
import numpy as np
from itertools import count


def create_input_field(id=None, value=None):
    field = document.createElement("input")
    field.type = "text"
    field.setAttribute("class", "form-control-sm mb-2 row")

    if id:
        field.id = id
    if value:
        field.value = value
    return field

def create_button(textContent, id, className):

    button = document.createElement("button")
    button.type = "button"
    button.textContent = textContent
    button.id = id
    button.setAttribute("class", className)
    return button


async def make_request(url, method, body=None, headers=None):

    csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value

    default_headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
        "ManageAssert": "False",
    }

    if headers:
        default_headers.update(headers)

    response = await pyfetch(url=url, method=method, body=body, headers=default_headers)

    if not 200 <= response.status < 300:
        default_headers.update({"ManageAssert": "True"})
        response = await pyfetch(
            url=url, method=method, body=body, headers=default_headers
        )
        return await response.json()

    if response.status == 204:
        return

    return await response.json()


def read_download_form():
    global fragment, form_loc, templateForm
    form_loc.textContent = ""
    templateForm.querySelector("#form").textContent = ""

    field_personal_id = create_input_field(id="id")
    field_name = create_input_field(id="name")
    field_last_name = create_input_field(id="last_name")
    field_age = create_input_field(id="age")

    field_personal_id.placeholder = "id (* to match the rest)"
    field_name.placeholder = "name"
    field_last_name.placeholder = "last name"
    field_age.placeholder = "age"

    search = create_button("Search", "search", "btn btn-primary btn-sm mx-2")
    export = create_button("Export", "export", "btn btn-primary btn-sm mx-2")

    templateForm.querySelector(".card-title").textContent = "Search and Export"
    templateForm.querySelector("#form").dataset.id = "action-1"
    templateForm.querySelector("#form").appendChild(field_personal_id)
    templateForm.querySelector("#form").appendChild(field_name)
    templateForm.querySelector("#form").appendChild(field_last_name)
    templateForm.querySelector("#form").appendChild(field_age)
    templateForm.querySelector("#form").appendChild(search)
    templateForm.querySelector("#form").appendChild(export)
    console.log(templateForm.querySelector("#form"))

    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)
def create_form():
    global fragment, form_loc, templateForm
    form_loc.textContent = ""
    templateForm.querySelector("#form").textContent = ""

    field_personal_id = create_input_field(id="id")
    field_name = create_input_field(id="name")
    field_last_name = create_input_field(id="last_name")
    field_age = create_input_field(id="age")

    field_personal_id.placeholder = "id"
    field_name.placeholder = "name"
    field_last_name.placeholder = "last name"
    field_age.placeholder = "age"

    create = create_button("Create", "create", "btn btn-primary btn-sm mx-2")

    templateForm.querySelector(".card-title").textContent = "Create new profile"
    templateForm.querySelector("#form").dataset.id = "action-2"
    templateForm.querySelector("#form").appendChild(field_personal_id)
    templateForm.querySelector("#form").appendChild(field_name)
    templateForm.querySelector("#form").appendChild(field_last_name)
    templateForm.querySelector("#form").appendChild(field_age)
    templateForm.querySelector("#form").appendChild(create)
    console.log(templateForm.querySelector("#form"))

    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)
def update_delete_form():
    global fragment, form_loc, templateForm
    form_loc.textContent = ""
    templateForm.querySelector("#form").textContent = ""

    field_personal_id = create_input_field()
    field_personal_id.placeholder = "input exact id"

    update = create_button("Update", "update", "btn btn-primary btn-sm mx-2")
    delete = create_button("Delete", "delete", "btn btn-danger btn-sm mx-2")

    templateForm.querySelector(".card-title").textContent = "Update or Delete profile"
    templateForm.querySelector("#form").dataset.id = "action-3"
    templateForm.querySelector("#form").appendChild(field_personal_id)
    templateForm.querySelector("#form").appendChild(update)
    templateForm.querySelector("#form").appendChild(delete)
    console.log(templateForm.querySelector("#form"))

    clone = templateForm.cloneNode(True)
    fragment.appendChild(clone)
    form_loc.appendChild(fragment)

def proxy_container(e):
    global response_loc

    if (
        e.target.id == "read-download-form"
        or e.target.id == "create-form"
        or e.target.id == "update-delete-form"
    ):
        console.log(e.target)
        console.log(e.target.id)
        response_loc.textContent = ""

    if e.target.id == "read-download-form":
        read_download_form()

    elif e.target.id == "create-form":
        create_form()

    elif e.target.id == "update-delete-form":
        update_delete_form()

    e.stopPropagation()


def errors_template(errors: dict):
    global templateDangerResponse, fragment, response_loc

    response_loc.textContent = ""

    templateDangerResponse.querySelector("h5").textContent = "error in the data entered"

    string = "<b>- {}:</b> {}<br />"

    message = "the following errors were found:<br /><br />"

    for key, value in errors.items():
        message += string.format(key, value[0])

    templateDangerResponse.querySelector("p").innerHTML = message[:-1]

    clone = templateDangerResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)
def data_validation(data:dict):
    errors = {}
    for k, v in data.items():
        if k == "id":
            v = v.replace("-", "").replace(".", "").replace("*", "")
            if v!="":
                if not v.isdigit():
                    errors['personal_id'] = ["personal_id must be a number"]
        elif k == "age":
            if not v.isdigit():
                errors[k] = ["A valid integer is required."]
            # elif int(v) < 18:
            #     errors[k] = ["age must be greater than 18"]
        elif k == "name":
            if not v.isalpha():
                errors[k] = ["name must be a string"]
        elif k == "last_name":
            if not v.isalpha():
                errors[k] = ["last_name must be a string"]
    return errors

def search_template():
    """
    Esta función se encarga de crear el template ante la respuesta de presionar el botón "search"
    """
    global templateSearchResponse, fragment, response_loc
    global searchResponse, searchNormalizedResponse

    response_loc.textContent = ""
    templateSearchResponse.querySelector("#search-buttons").textContent = ""

    templateSearchResponse.querySelector("h5").textContent = "Total results: {}".format(
        searchResponse["count"].values[0]
    )

    console.log("Search Template")
    console.log(searchResponse.to_string())
    console.log(searchNormalizedResponse.to_string())

    templateSearchResponse.querySelector(
        "#response"
    ).innerHTML = searchNormalizedResponse.to_html(index=True, header=False)

    if str(searchResponse["previous"].values[0]) != "nan":
        previous = create_button(
            textContent="Previous Page",
            id="previous",
            className="btn btn-link btn-sm shadow m-2 p1 border border-primary",
        )
        templateSearchResponse.querySelector("#search-buttons").appendChild(previous)
    if str(searchResponse["next"].values[0]) != "nan":
        next = create_button(
            textContent="Next Page",
            id="next",
            className="btn btn-link btn-sm shadow m-2 p1 border border-primary",
        )
        templateSearchResponse.querySelector("#search-buttons").appendChild(next)

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

    console.log("search_data")

    personal_id = document.querySelectorAll(".form-control-sm")[0].value
    name = document.querySelectorAll(".form-control-sm")[1].value
    last_name = document.querySelectorAll(".form-control-sm")[2].value
    age = document.querySelectorAll(".form-control-sm")[3].value

    data = {"id": personal_id, "name": name, "last_name": last_name, "age": age}
    data = {key: value for key, value in data.items() if value != ""}
    
    # Validation 1
    if data == {}:
        errors_template({"fields": ["at least one field must be filled"]})
        return

    # Validation 2
    errors = data_validation(data)
    if errors != {}:
        errors_template(errors)
        return

    url = "http://localhost:8000/api/v1/profiles/?page=1&"
    for key, value in data.items():
        url += f"{key}={value}&"
    url = url[:-1]

    response = await make_request(url=url, method="GET")

    if response.get("errors"):
        errors_template(response["errors"])
    else:
        searchResponse = (
            pd.read_json(json.dumps(response))
            .loc[0, ["count", "next", "previous"]]
            .to_frame()
            .T
        )
        searchNormalizedResponse = pd.json_normalize(response, record_path=["results"])
        searchNormalizedResponse.index += 1
        search_template()


def export_success_template():
    global templateSuccessResponse, fragment, response_loc

    response_loc.textContent = ""

    templateSuccessResponse.querySelector("h5").textContent = "download successfull"

    clone = templateSuccessResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)
async def export_data(e):
    global response_loc
    console.log("export_data")

    response_loc.textContent = ""

    personal_id = document.querySelectorAll(".form-control-sm")[0].value
    name = document.querySelectorAll(".form-control-sm")[1].value
    last_name = document.querySelectorAll(".form-control-sm")[2].value
    age = document.querySelectorAll(".form-control-sm")[3].value

    data = {"id": personal_id, "name": name, "last_name": last_name, "age": age}
    data = {key: value for key, value in data.items() if value != ""}


    # Validation 1
    if data == {}:
        errors_template({"fields": ["at least one field must be filled"]})
        return

    # Validation 2
    errors = data_validation(data)
    if errors != {}:
        errors_template(errors)
        return

    # Make request
    url = "http://localhost:8000/api/v1/contents/?"
    for key, value in data.items():
        url += f"{key}={value}&"
    url = url[:-1]

    a = document.createElement("a")
    a.href = url
    a.download = "export-failed.csv"
    a.click()

    export_success_template()


def create_success_template():
    """
    Esta función se encarga de crear el template ante la respuesta de presionar el botón "create"
    """
    global templateSuccessResponse, fragment, response_loc

    response_loc.textContent = ""

    personal_id = document.getElementById("id")
    name = document.getElementById("name")
    last_name = document.getElementById("last_name")
    age = document.getElementById("age")

    personal_id.value = ""
    name.value = ""
    last_name.value = ""
    age.value = ""

    templateSuccessResponse.querySelector(
        "h5"
    ).textContent = "Profile created successfully!"

    clone = templateSuccessResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)
async def create_data(e):

    console.log("create_data")
    # console.log('1', e.target.parentElement)

    personal_id_input = document.querySelectorAll(".form-control-sm")[0].value
    name_input = document.querySelectorAll(".form-control-sm")[1].value
    last_name_input = document.querySelectorAll(".form-control-sm")[2].value
    age_input = document.querySelectorAll(".form-control-sm")[3].value

    data = {
        "personal_id": personal_id_input,
        "name": name_input,
        "last_name": last_name_input,
        "age": age_input,
    }

    url = "http://localhost:8000/api/v1/profiles/"
    body = json.dumps(data)

    response = await make_request(url=url, method="POST", body=body)

    if response.get("errors"):
        errors = response.get("errors")
        errors_template(errors)

    else:
        create_success_template()


def update_search_template(data: dict):
    global response_loc, fragment, templateUpdateResponse
    console.log("search profile success")

    response_loc.textContent = ""
    templateUpdateResponse.querySelector("div").textContent = ""

    personal_id = create_input_field(id='id', value=data['personal_id'])
    name = create_input_field(id='name', value=data['name'])
    last_name = create_input_field(id='last_name', value=data['last_name'])
    age = create_input_field(id='age', value=data['age'])

    confirm = create_button(
        textContent="Confirm",
        id="confirm",
        className="btn btn-primary btn-sm shadow m-2 p1",
    ) 
    
    templateUpdateResponse.querySelector("h5").textContent = "Update profile"
    templateUpdateResponse.querySelector("div").appendChild(personal_id)
    templateUpdateResponse.querySelector("div").appendChild(name)
    templateUpdateResponse.querySelector("div").appendChild(last_name)
    templateUpdateResponse.querySelector("div").appendChild(age)
    templateUpdateResponse.querySelector("div").appendChild(confirm)

    clone = templateUpdateResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)

    confirm.addEventListener('click', create_proxy(update_confirm))

async def update_data(e):

    console.log("update_data")

    personal_id = document.querySelectorAll(".form-control-sm")[0]
    personal_id_input = personal_id.value

    if personal_id_input == "":
        errors = {"personal_id": ["This field is required"]}
        return errors_template(errors)

    response = await make_request(
        url="http://localhost:8000/api/v1/profiles/{}/".format(personal_id_input),
        method="GET",
    )

    if response.get("errors"):
        errors = response.get("errors")
        errors_template(errors)

    else:
        update_search_template(response)


def delete_search_template(data: dict):
    global templateSearchResponse, fragment, response_loc

    response_loc.textContent = ""
    templateSearchResponse.querySelector("#search-buttons").textContent = ""

    templateSearchResponse.querySelector("h5").textContent = "Confirm delete?"

    templateSearchResponse.querySelector(
        "#response"
    ).innerHTML = """
        <tr>
            <td> </td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
    """.format(
        data.get("personal_id"),
        data.get("name"),
        data.get("last_name"),
        data.get("age"),
    )

    confirm = create_button(
        textContent="Confirm",
        id="confirm",
        className="btn btn-danger btn-sm shadow m-2 p1",
    )  # , onclick='delete_data')

    templateSearchResponse.querySelector("#search-buttons").appendChild(confirm)

    clone = templateSearchResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)
async def delete_data(e):
    global templateForm
    console.log("delete_data")

    personal_id = document.querySelectorAll(".form-control-sm")[0]
    personal_id_input = personal_id.value

    if personal_id_input == "":
        errors = {"personal_id": ["This field is required"]}
        return errors_template(errors)

    response = await make_request(
        url="http://localhost:8000/api/v1/profiles/{}/".format(personal_id_input),
        method="GET",
    )

    if response.get("errors"):
        errors = response.get("errors")
        errors_template(errors)
    else:
        delete_search_template(response)

async def proxy_form_location(e):
    global templateForm

    action = templateForm.querySelector("#form").dataset.id
    button_id = e.target.id

    if action == "action-1" and button_id == "search":
        console.log(e.target)
        await search_data(e)

    elif action == "action-1" and button_id == "export":
        console.log(e.target)
        await export_data(e)

    elif action == "action-2" and button_id == "create":
        console.log(e.target)
        await create_data(e)

    elif action == "action-3" and button_id == "update":
        console.log(e.target)
        await update_data(e)

    elif action == "action-3" and button_id == "delete":
        console.log(e.target)
        await delete_data(e)

    e.stopPropagation()

def update_success_template():
    global templateSuccessResponse, fragment, response_loc

    response_loc.textContent = ""

    templateSuccessResponse.querySelector(
        "h5"
    ).textContent = "Profile updated successfully!"

    clone = templateSuccessResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)

    update_delete_form()
async def update_confirm(e):
    global templateUpdateResponse
    console.log('update_confirm')
    console.log(e.target)
    console.log(templateUpdateResponse)
    console.log(templateUpdateResponse.getElementById('id'))
    console.log(templateUpdateResponse.getElementById('name'))
    console.log(templateUpdateResponse.getElementById('last_name'))
    console.log(templateUpdateResponse.getElementById('age'))

    id_url = templateUpdateResponse.getElementById('id').value
    personal_id = document.getElementById('id').value
    name = document.getElementById('name').value
    last_name = document.getElementById('last_name').value
    age = document.getElementById('age').value

    data = {
        "personal_id": personal_id,
        "name": name,
        "last_name": last_name,
        "age": age,
    }

    url = "http://localhost:8000/api/v1/profiles/{}/".format(id_url)
    body = json.dumps(data)

    response = await make_request(url=url, method="PUT", body=body)
    
    if response.get("errors"):
        errors = response.get("errors")
        errors_template(errors)

    else:
        console.log('profile updated successfully')
        update_success_template()

def delete_success_template():
    global templateSuccessResponse, fragment, response_loc

    response_loc.textContent = ""

    templateSuccessResponse.querySelector(
        "h5"
    ).textContent = "Profile deleted successfully!"

    clone = templateSuccessResponse.cloneNode(True)
    fragment.appendChild(clone)
    response_loc.appendChild(fragment)

    update_delete_form()
async def delete_confirm(e):
    console.log("delete_confirm")

    personal_id = document.querySelectorAll(".form-control-sm")[0].value
    console.log(personal_id)
    if personal_id == "":
        errors = {"personal_id": ["This field is required"]}
        return errors_template(errors)

    response = await make_request(
        url="http://localhost:8000/api/v1/profiles/{}/".format(personal_id),
        method="DELETE",
    )

    delete_success_template()

async def change_page(e, forward):
    """
    Esta función se encarga de hacer el request con la nueva página
    """
    global searchResponse, searchNormalizedResponse, x
    console.log("change_page")

    if forward:
        console.log("forward")
        response = await make_request(url=searchResponse["next"][0], method="GET")

    else:
        console.log("back")
        response = await make_request(url=searchResponse["previous"][0], method="GET")
    console.log(json.dumps(response))

    searchResponse = (
        pd.read_json(json.dumps(response))
        .loc[0, ["count", "next", "previous"]]
        .to_frame()
        .T
    )
    searchNormalizedResponse = pd.json_normalize(response, record_path=["results"])
    searchNormalizedResponse.index += 1
    if forward:
        x += 1
        searchNormalizedResponse.index += 5 * x
    else:
        x -= 1
        searchNormalizedResponse.index += 5 * x

    search_template()

async def proxy_response_location(e):
    global templateSearchResponse, response_loc

    if e.target.id == "previous" or e.target.id == "next" or e.target.id == "confirm":
        console.log(e.target)

    if e.target.id == "previous":
        console.log("previous")
        await change_page(e, forward=False)

    elif e.target.id == "next":
        console.log("next")
        await change_page(e, forward=True)

    elif e.target.id == "confirm":
        console.log("confirm")
        if e.target.classList.contains("btn-danger"):
            await delete_confirm(e)
        elif e.target.classList.contains("btn-primary"):
            await update_confirm(e)

    e.stopPropagation()


def main():
    # created in HTML
    global container, form_loc, response_loc
    global templateForm, templateSearchResponse, templateUpdateResponse, templateSuccessResponse, templateDangerResponse

    # created localy
    global fragment, searchResponse, searchNormalizedResponse, x

    x = 0
    fragment = document.createDocumentFragment()
    searchResponse = pd.DataFrame()
    searchNormalizedResponse = pd.DataFrame()

    container = document.querySelector(".container")
    form_loc = document.querySelector("#form-loc")
    response_loc = document.querySelector("#response-loc")
    templateForm = document.getElementById("template-form").content
    templateSearchResponse = document.getElementById("template-search-response").content
    templateUpdateResponse = document.getElementById("template-update-response").content
    templateSuccessResponse = document.getElementById(
        "template-success-response"
    ).content
    templateDangerResponse = document.getElementById("template-danger-response").content

    container.addEventListener("click", create_proxy(proxy_container))

    form_loc.addEventListener("click", create_proxy(proxy_form_location))

    response_loc.addEventListener("click", create_proxy(proxy_response_location))


main()
