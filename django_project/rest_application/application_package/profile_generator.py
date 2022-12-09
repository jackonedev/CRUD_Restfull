import os, random, pprint, json
from itertools import count


def get_profile(age_input=None):
    "Funcion que retorna un diccionario con los datos de una persona genérica"
    age = age_input or get_random_age()
    id = get_id(age)
    name, last_name = get_random_name()
    return {'personal_id': id, 'name': name, 'last_name': last_name, 'age': age}


def get_random_age():
    return random.randint(18, 100)

def recta_id_coef(age):
    if age >= 18 and age <= 36:
        x1, x2 = 18, 36
        y1, y2 = 3e6, 900000

    if age > 36 and age <= 65:
        x1, x2 = 37, 65
        y1, y2 = 760000, 250000

    if age > 65 and age <= 100:
        x1, x2 = 66, 100
        y1, y2 = 162000, 55000
    return int((y2 - y1) / (x2 - x1) * (age - x1) + y1)

def get_id(age):
    global counter
    root_id = recta_id_coef(age) * age
    plus = next(counter)
    return root_id + plus
    

def get_files(path):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files


def get_directories(path):
    directories = []
    for directory in os.listdir(path):
        if os.path.isdir(os.path.join(path, directory)):
            directories.append(directory)
    return directories


def get_random_name():
    name = random.choice(["Juan", "Pedro", "Maria", "Alejandra", "Jorge", "Mario", "Sofia", "Carola", "Agustin", "Victoria"])
    last_name = random.choice(["Gris", "Azul", "Verde", "Amarillo", "Rojo", "Naranja", "Violeta", "Bordo"])
    return name, last_name


def main():
    global counter
    counter = count()
    
    def test_1():
        for i in range(10):
            print (">>>> Generated Profile:")
            print(get_profile())
            print()

    def test_2():
        print (get_profile(age_input=32))
        print (get_profile(age_input=36))
        print (get_profile(age_input=37))
        print (get_profile(age_input=65))
        print (get_profile(age_input=66))

    # test_1()
    # test_2()

    
main()