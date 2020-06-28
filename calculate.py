import toml
import qsml
import requests
from tabulate import tabulate

secrets_file = "data/secrets.toml"
secrets = toml.load(secrets_file)

token = secrets["hidden"]["token"]

qsml_file = "data/data.qsml"
data = qsml.load(qsml_file)

table = []
headers = ["SYM", "SHARES", "PRICE", "TOTAL"]

# "ensureTwoDecimals" (FLOAT ONLY)
def e2D(val):
    return "${:.2f}".format(val)


def calculatePortfolioValuation(api_data, qsml_data):
    total = 0
    for stock, amt in qsml_data["main"].items():
        for quote in api_data.values():
            if stock == quote["quote"]["symbol"]:
                p = quote["quote"]["latestPrice"]
                tmp = [stock, amt, e2D(p), e2D(p * amt)]
                table.append(tmp)
                total += float(amt) * p

    print('Valuation for group "%s"' % "main")
    print(tabulate(table, headers, tablefmt="pretty"))
    print("Total Portfolio value: ${:.2f}".format(total))


lst = ""  # initialize url list of stocks

for stock, amt in data["main"].items():
    lst += "%s," % stock

lst = lst[:-1]  # trim trailing comma

url = f"https://cloud.iexapis.com/stable/stock/market/batch?symbols={lst}&types=quote&range=1m&token={token}"

r = requests.get(url)
json_obj = r.json()

calculatePortfolioValuation(json_obj, data)
