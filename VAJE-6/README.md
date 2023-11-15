# Vaja - RPC client

Izdelali bomo preprost rpc client z uporabo knjižnice requests. Na koncu če bomo imeli čas si bomo ogledali kako lahko nastalo kodo še dodatno optimiziramo tako da uporabimo async  in batching metodi. 

Dokumentacija RPC api-ja: https://ethereum.github.io/execution-apis/api-documentation/

Install requests library: pip install requests

## Prvi del - samostojna izdelava klienta (zaprosimo za zadnji blok)

- Definiramo variable, ki so potrebne za request (POST)
- Pošljemo request
- Preverimo če je odgovor pravilen, ter shranimo odgovor v json (if pravilen)

#### Implementiraj kodo (pomagaj si z comments)
```python
import requests
import json
# definiraj VARIABLE nase skripte
    # API URL od infure za Ethereum mainnet


    # JSON-RPC request payload  (pogledamo dokumentacijo!)


    # Nastavimo headerje za JSON-RPC request


# Pošljemo request (uporabimo requests.post mdetodo)


# Error handling. POgledamo če smo dobili pravilen odgovor.
    # ce ni error-ja (status code 200) sprintamo sporocilo in shranimo dobljeno sporocilo v json

    # else, sprintaj sporocilo da nam ni uspelo dobiti zadnji block in dodaj kateri error oz. code-status code smo dobili
```

## Drugi del - delo s podatki (block_data.json)

V bloku imamo del kjer so zapisane transakcije, naša naloga je, da preštejemo koliko je teh transakcij.

```python
# naredimo kopijo podatkov - .copy() metoda


# definiramo counter


# Iteriramo čez transakcije in povečujemo counter


# Izpišemo/sprintamo counter (število transakcij)


```


##  Tretji del - DODATNA VAJA ni obezna - izluščimo vse naslove (from, to) iz transakcij

V vsaki transakciji imamo definirana naslova pošiljalca ("from") in prejemnika ("to"). Naša naloga je, da izluščimo vse naslove in jih shranimo v dictionary kot ključe (key). Za vrednosti (value) pa zaenkrat zapisemo vrednost None.

```python
# naredimo kopijo podatkov - .copy() metoda


# definiramo dictionary za shranjevanje naslovov


# iteriramo čez transakcije in izluščimo naslove (.get("from")   .get("to")) in jih shranimo v dictionary


# sprintamo dictionary

```
## Četrti del - refactoring

Do sedaj spisano kodo spravite v funkciji in nato napisite se main() funkcijo ki klice funkciji v pravilnem vrstnem redu. Rezultat je bolj pregledna in modularna skripta.

- Kodo do zdaj spravi v funkciji
- Napiši še dodatno funkcijo main() ki bo klicala obe funkciji v pravilnem vrstnem redu
    - npr. 1. funkcija getBlock 2. funkcija steviloTransakcij ali izlusciNaslove





