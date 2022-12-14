def get_query_params(request, model):
    id = request.query_params.get("id", None)
    name = request.query_params.get("name", None)
    last_name = request.query_params.get("last_name", None)
    age = request.query_params.get("age", None)


    # Validacion 1
    if not (name or last_name or age or id):
        return 1 / 0

    query_params = {
        "id": id,
        "name": name,
        "last_name": last_name,
        "age": age,
    }

    # Validacion 2
    query_params = {k: v for k, v in query_params.items() if v is not None}

    for k, v in query_params.items():
        if k == "id":
            if not v.isdigit():
                return "bad request"
        elif k == "age":
            if not v.isdigit():
                return "bad request"
        elif k == "name":
            if v.isdigit():
                return "bad request"
        elif k == "last_name":
            if v.isdigit():
                return "bad request"

    # Validacion 3
    if id:
        if not id.startswith("*") and not id.endswith("*"):
            profiles = model.objects.filter(personal_id=id)
        elif id.startswith("*") and id.endswith("*"):
            id = id.replace("*", "")
            profiles = model.objects.filter(personal_id__icontains=id)
        elif id.startswith("*"):
            id = id.replace("*", "")
            profiles = model.objects.filter(personal_id__iendswith=id)
        elif id.endswith("*"):
            id = id.replace("*", "")
            profiles = model.objects.filter(personal_id__istartswith=id)
        if len(profiles) == 0:
            profiles = "not found"

        return profiles

    # Validacion 4
    try:
        name = name.title()
    except:
        pass
    try:
        last_name = last_name.title()
    except:
        pass
    try:
        if name and last_name and age:
            profiles = model.objects.filter(name=name, last_name=last_name, age=age)
        elif name and last_name:
            profiles = model.objects.filter(name=name, last_name=last_name)
        elif name and age:
            profiles = model.objects.filter(name=name, age=age)
        elif last_name and age:
            profiles = model.objects.filter(last_name=last_name, age=age)
        elif name:
            profiles = model.objects.filter(name=name)
        elif last_name:
            profiles = model.objects.filter(last_name=last_name)
        elif age:
            profiles = model.objects.filter(age=age)
        else:
            profiles = "not found"
        if len(profiles) == 0:
            profiles = "not found"
        return profiles

    except:
        profile = "bad request"
        return profile
