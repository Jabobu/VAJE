# OPtimizacija kode

spodnja koda predstavlja celoten potek nasega preprostega programa. 
- dobimo zadnji blok
- izluscimo naslove iz transakcij
- iteriramo cez naslove in za vsakega naredimo request getBalance (dobimo trenutno stevilo ETH kovancev za vse racune)

```python

import requests
import json
#PART1 (get the lastest block)

# VARIABLE nase skripte
# API URL od infure za Ethereum mainnet
node_url = "https://mainnet.infura.io/v3/fae3809fae484184b3de1354e592d12c"
# Dictionary kjer bomo spravili naslove
addresses = {}

# JSON-RPC request payload  (pogledamo dokumentacijo!)
payload = {
    "method": "eth_getBlockByNumber",
    "params": ["latest", True],  # "latest" for the latest block, True to get full transaction objects
    "jsonrpc": "2.0",
    "id": 1,
}

# Set the appropriate headers for JSON-RPC request??
headers = {
    "Content-Type": "application/json",
}

# Posljemo request
response = requests.post(node_url, data=json.dumps(payload), headers=headers)

# pogledamo ce smo dobili pravilen odgovor, ce ja sprintamo json IN shranimo, ce ne vrzemo kateri error smo dobili
if response.status_code == 200:
    # Parsamo response JSON
    block_data = response.json()
    print("Dobili smo blok!")
    #print(json.dumps(block_data, indent=4))
    with open('blockData.json', 'w', encoding='utf-8') as f:
        json.dump(block_data, f, ensure_ascii=False, indent=4)
else:
    print(f"Nismo dobili bloka. Statusna koda: {response.status_code}")
    
#PART 2 (extract the addresses from the block data and pupolate a dictionary)
# spodnja vrstica ni nujno potrebna (samo ce hocemo )
data = block_data.copy()

# Iteriramo cez transakcije v bloku in izluscimo vse naslove 
for transaction in data["result"]["transactions"]:
    from_address = transaction.get("from")
    to_address = transaction.get("to")

    # dodamo naslove v addresses dictionary
    if from_address:
        addresses[from_address] = None
    if to_address:
        addresses[to_address] = None

print("izluscili smo naslove")

#PART 3 (Posodobimo nas addresses dictionary tako da vsakemo naslovu dodamo vrednost (stevilo ETH kovancev))
# Zdaj ko imamo dictionary kjer imamo vse naslove kot keys in prazne vrednosti kot values, lahko pošljemo requeste na rpc za balance teh naslovov. DObljene odgovore za vsak naslov shranimo kot values v dictionary.
# Iteriramo cez naslove in naredimo requeste na rpc node (eth_getBalance)
for address in addresses.keys():
    # JSON-RPC request payload za  getBalance
    payload = {
        "method": "eth_getBalance",
        "params": [address, "latest"],  # latest block - zadnji blok (poglej dokumentacijo za vec info)
        "jsonrpc": "2.0",
        "id": 1,
    }

    # Posljemo request
    response = requests.post(node_url, data=json.dumps(payload), headers=headers)

    # Error handling - preverimo ce smo dobili pravilen odgovor
    if response.status_code == 200:
        response_data = response.json()
        balance = response_data.get("result")
        # posodibimo dictionary s dobljeno vrednostjo
        addresses[address] = balance
        print("balance dodan za: ", address)
    else:
        print(f"Nismo dobili eth balance za naslov {address}. Status code: {response.status_code}")

# Sprintamo posodobljen dictionary
print(addresses)


```


Pri requestih za pridobivanje balance-a smo opazili, da je delovanje zelo počasno. Razlog je, da smo skirpto spisali na sinhroni način, sepravi za vsak naslov naredimo svoj request in izvrševanje kode se zaustavi dokler ne dobimo nazaj odgovora.

Problem lahko rešujemo na dva načina in sicer tako da preuredimo kodo na asynhron nacin in tako da requeste za vsak naslov zdruzimo skupaj v "batch". 


## Asynchrounous requests

Asinhroni zahtevki so močna lastnost v programiranju, ki vam omogoča izvajanje več operacij hkrati (sočasno) brez čakanja, da se vsaka operacija zaporedno zaključi. To je še posebej uporabno v scenarijih, kot so omrežni zahtevki, kjer se čas odziva lahko razlikuje in lahko vključuje čakanje (na primer, čakanje na odgovor strežnika).

V kontekstu našega programa, izvajanje asinhronih zahtev za pridobivanje podatkov iz Ethereum verige pomeni, da vam ni treba čakati na odgovor nekega zahtevka, preden začnete naslendji zahtevek. Namesto tega lahko skoraj sočasno pošiljate več zahtev in obdelujete njihove odgovore, ko prihajajo, kar je lahko veliko hitreje, kot čakanje, da se vsaka zahteva zaključi zaporedno.

Kako delujejo asinhroni zahtevi v našem skriptu:

1. **Asinhronne funkcije z `async`:** Funkcije, ki izvajajo asinhrone operacije, so opredeljene z besedo `async`. Te funkcije, znane kot "coroutines", se lahko zaustavijo in ponovno zacnejo/nadaljujejo.

2. **Čakanje odgovorov z `await`:** V asinhroni funkciji uporabimo `await` za začasno ustavitev izvajanja, dokler se ne zaključi funkcija, na katero čakamo. To ne ustavi celotnega programa. Medtem ko je ena sokorutina oz. asinhrona funkcija zaustavljena in čaka na odgovor, lahko druge sokorutine tečejo.

3. **Sočasno izvajanje z `asyncio.gather`:** Funkcija `asyncio.gather()` se uporablja za sočasno izvajanje več sokorutin. Čaka, da se vse zaključijo in nato zbira njihove rezultate. V našem primeru je vsak http zahtevek  sokorutina.

4. **Dogodkovna zanka z `asyncio.run`:**  To je osnova asinhronega izvajanja, ki upravlja sokorutine. Z njo začnemo asinhroni program.

Ko uporabljate ta pristop za izvajanje omrežnih zahtev, naš program pošlje vse zahtevke hkrati (skoraj). Med čakanjem na odgovor od enega zahtevka vaš program ne sedi neaktivno; nadaljuje z pošiljanjem več zahtevkov. Ko odgovori začnejo prihajati nazaj, se vsak `await`ed klic nadaljuje tam, kjer se je ustavil, obdela odgovor in sokorutina se zaključi. Ta sočasna obdelava zahtev lahko znatno zmanjša skupni čas, ki je potreben v primerjavi s sinhronim pristopom, kjer bi moral vsak zahtevek čakati, da se prejšnji zaključi.

!!Ne pozabite, asinhrono programiranje lahko vpelje kompleksnosti, še posebej glede obvladovanja napak in razumevanja toka programa, vendar je zelo učinkovito za naloge, kot je izvajanje več omrežnih zahtevkov!!


```python
import aiohttp
import asyncio
import json

import nest_asyncio
nest_asyncio.apply()

node_url = "https://mainnet.infura.io/v3/fae3809fae484184b3de1354e592d12c"

headers = {
    "Content-Type": "application/json",
}

async def fetch_block():
    payload = {
        "method": "eth_getBlockByNumber",
        "params": ["latest", True],
        "jsonrpc": "2.0",
        "id": 1,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(node_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data["result"]["transactions"]
            else:
                raise Exception(f"Error fetching block: {response.status}")

async def fetch_balance(address):
    payload = {
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "jsonrpc": "2.0",
        "id": 1,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(node_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data["result"]
            else:
                raise Exception(f"Error fetching balance for {address}: {response.status}")

async def main():
    transactions = await fetch_block()
    addresses = {tx.get("from"): None for tx in transactions if tx.get("from")}
    addresses.update({tx.get("to"): None for tx in transactions if tx.get("to")})

    balance_tasks = [fetch_balance(address) for address in addresses]
    balances = await asyncio.gather(*balance_tasks)

    for address, balance in zip(addresses, balances):
        addresses[address] = int(balance,0)/10**18

    print(type(addresses))
    for key,value in addresses.items():
        print(key, "has", value, "ETH")

await main()

```


## Batching requests

Skupinsko pošiljanje zahtevkov (angl. batching) je tehnika, ki omogoča pošiljanje več zahtevkov v enem samem omrežnem klicu. To je koristno, še posebej pri interakciji z omrežnimi vmesniki, kot so RPC (Remote Procedure Call) vozlišča, kjer lahko zmanjša omrežno obremenitev.

V kontekstu Ethereum RPC, kot ga uporablja Infura, skupinsko pošiljanje zahtev omogoča, da pošljemo več poizvedb, kot so zahtevki za stanje (npr. getBalance), v enem samem HTTP zahtevku. To ni del samega RPC protokola, ampak funkcionalnost, ki jo vozlišče (kot je Infura) lahko omogoči. Z drugimi besedami, moznost batching-a je odvisna od implementacije na strani strežnika.

V našem primeru postopek/skripta deluje tako:

1. Najprej pošljemo zahtevek za pridobitev najnovejšega bloka. Iz bloka nato izluscimo naslove.

2. Ustvarimo skupinski zahtevek, kjer za vsak naslov ustvarimo posamezen zahtevek za pridobivanje stanja (getBalance). Ti posamezni zahtevki so združeni v en skupni JSON zahtevek.

3. Ta skupinski zahtevek pošljemo na Ethereum vozlišče. Vozlišče obdela vse zahtevke v paketu in vrne odgovore za vsakega od njih v enem samem odgovoru.


Ta pristop je učinkovit, ker zmanjšuje število omrežnih klicev, potrebnih za pridobivanje informacij o več naslovih. Namesto več posamičnih zahtevkov pošljemo en sam skupinski zahtevek, kar je še posebej koristno pri velikih količinah zahtevkov ali omejenem številu dovoljenih zahtevkov na vozlišče.

```python
import requests
import json

addresses = {}
updated_addresses = {}

def fetch_latest_block(node_url, headers):
    payload = {
        "method": "eth_getBlockByNumber",
        "params": ["latest", True],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(node_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch the latest block. Status code: {response.status_code}")

def extract_addresses(block_data):
    addresses = {}
    for transaction in block_data["result"]["transactions"]:
        from_address = transaction.get("from")
        to_address = transaction.get("to")
        if from_address:
            addresses[from_address] = None
        if to_address:
            addresses[to_address] = None
    return addresses

def fetch_balances_batch(node_url, headers, addresses):
    batch_payload = [{"jsonrpc": "2.0", "id": i, "method": "eth_getBalance", "params": [address, "latest"]}
                     for i, address in enumerate(addresses.keys(), 1)]
    response = requests.post(node_url, json=batch_payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        updated_addresses = {}
        for item in response_data:
            address = list(addresses.keys())[item['id'] - 1]
            updated_addresses[address] = int(item['result'], 0) / 10**18
        return updated_addresses
    else:
        raise Exception(f"Failed to fetch balances. Status code: {response.status_code}")

def main():
    node_url = "https://mainnet.infura.io/v3/fae3809fae484184b3de1354e592d12c"
    headers = {"Content-Type": "application/json"}
    global addresses
    global updated_addresses
    
    try:
        block_data = fetch_latest_block(node_url, headers)
        addresses = extract_addresses(block_data)
        updated_addresses = fetch_balances_batch(node_url, headers, addresses)
        print(updated_addresses)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

```

