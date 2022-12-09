import pandas as pd


def to_pandas(model):
    data = model.objects.all().values()
    df = pd.DataFrame(data)
    return df