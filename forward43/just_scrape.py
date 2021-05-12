import requests

id_range    = range(1, 99999)
ids         = [str(i).zfill(5) for i in id_range]

print(ids[0:10])