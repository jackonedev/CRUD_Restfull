def get_query_params(request, model):
    name = request.query_params.get('name', None)
    last_name = request.query_params.get('last_name', None)
    age = request.query_params.get('age', None)

    if not (name or last_name or age):
        return 1/0


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
            profiles = 'not found'
        if len(profiles) == 0:
            profiles = 'not found'
        return profiles
    
    except:
        profile = 'bad request'
        return profile