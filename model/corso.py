from dataclasses import dataclass


@dataclass
class Corso:
    codins: str
    crediti: int
    nome: str
    pd: int

    def __eq__(self, other):
        return self.codins == other.codins # codins perche questo metodo paragona solo le chiavi primarie

    def __hash__(self):
        return hash(self.codins) # DI nuovo, chiave primaria per il metodo hash

    def __str__(self): # questa è la stampa
        return f"{self.nome} ({self.codins}) - {self.crediti} CFU"