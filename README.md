# Įvadas

Šio kursinio darbo tikslas sukurti kompiuterinį žaidimą “Laivų mūšis”. Šiame žaidime žaidėjas spėlioja priešininko laivų koordinates, laimi tas, kuris pirmas nuskandina visus laivus.

Norint paleisti žaidimą reikia turėti python programą, tada parsisiųsti `main.py`, bei `winner.txt` ir `grid_size.txt` failus ir juos sudėti viename aplanke, tada paleisti `main.py` ir spausti „run“. Taip pat iš `main.py` galima sukurti `.exe` failą, kurio dėka nereiktų turėti python programos.

Žaidimo eiga paprasta – reikia spausti ant priešininko žemėlapio langelių, paspaudus užsidega žalia arba raudona spalva ir atitinkamai raidės **X** arba **N**, žalia spalva reiškia pataikymą, raudona – nepataikymą. Žaidėjas žaidžia prieš kompiuterį. Nuskendus visiems laivams iššoka langelis ir informuoja apie laimėtoją.

---

# Analizė

**Ship** klasė naudoja metodus sekti smūgių skaičių ir tikrinti ar laivas nuskendo.

Subklasės (**Carrier**, **Destroyer**, **Submarine**, **Battleship**, **Cruiser**) paveldi savybes iš `Ship` klasės, nurodo savo dydžius.

`GUI` klasėje aprašytas visas žaidimo veikimo principas, sukuriamas langas, langeliai, iš failo `grid_size.txt` paimamas žemėlapio dydis.

---

## Polimorfizmas

`Ship` klasė turi bendrą metodą `ship_sunk`. Kiekviena `Ship` subklasė turi savo specifinius parametrus šiam metodui (skirtingas dydis).

```py
class Ship:
def __init__(self, size):
    self.size = size
    self.hit_count = 0

    def ship_sunk(self):
        return self.hit_count >= self.size


class Carrier(Ship):
    def __init__(self):
        super().__init__(size=5)


class Battleship(Ship):
    def __init__(self):
        super().__init__(size=4)


class Cruiser(Ship):
    def __init__(self):
        super().__init__(size=3)


class Submarine(Ship):
    def __init__(self):
        super().__init__(size=3)


class Destroyer(Ship):
    def __init__(self):
        super().__init__(size=2)
```

---

## Abstrakcija

`Ship` klasė apibrėžia abstrakčią laivo sąvoką su bendromis savybėmis (`size`, `hit_count`) ir metodais (`ship_sunk()`), bet konkrečius laivų tipus apibrėžia subklasės. `GUI` klasėje žaidimo logika (pvz., laivų statymas, šūvių apdorojimas) yra abstraktuota į atskirus metodus, kuriuos vartotojas mato kaip vieną visumą.

```py
class Ship:
def __init__(self, size):
    self.size = size
    self.hit_count = 0

    def ship_sunk(self):
        return self.hit_count >= self.size


class Carrier(Ship):
    def __init__(self):
        super().__init__(size=5)


class Battleship(Ship):
    def __init__(self):
        super().__init__(size=4)


class Cruiser(Ship):
    def __init__(self):
        super().__init__(size=3)


class Submarine(Ship):
    def __init__(self):
        super().__init__(size=3)


class Destroyer(Ship):
    def __init__(self):
        super().__init__(size=2)
```


---

## Paveldėjimas

Visi konkretūs laivų tipai (**Carrier**, **Battleship**, **Cruiser**, **Submarine**, **Destroyer**) paveldi savybes iš bazinės `Ship` klasės. Paveldimos visos bazinės klasės savybės (`size`, `hit_count`) ir metodai (`ship_sunk()`). Kiekviena subklasė savo konstruktoriuje nurodo konkretų laivo dydį, perduodant jį klasės konstruktoriui per `super().__init__()`.

```py
class Ship:
def __init__(self, size):
    self.size = size
    self.hit_count = 0

    def ship_sunk(self):
            return self.hit_count >= self.size


class Carrier(Ship):
    def __init__(self):
        super().__init__(size=5)


class Battleship(Ship):
    def __init__(self):
        super().__init__(size=4)


class Cruiser(Ship):
    def __init__(self):
        super().__init__(size=3)


class Submarine(Ship):
    def __init__(self):
        super().__init__(size=3)


class Destroyer(Ship):
    def __init__(self):
        super().__init__(size=2)
```


---

## Inkapsuliacija

`Ship` klasė inkapsuliuoja laivų kūrimo logiką – `super().__init__` konstruktorius yra privatus metodas

```python
class Ship:
def __init__(self, size):
    self.size = size
    self.hit_count = 0

    def ship_sunk(self):
            return self.hit_count >= self.size


class Carrier(Ship):
    def __init__(self):
        super().__init__(size=5)


class Battleship(Ship):
    def __init__(self):
        super().__init__(size=4)


class Cruiser(Ship):
    def __init__(self):
        super().__init__(size=3)


class Submarine(Ship):
    def __init__(self):
        super().__init__(size=3)


class Destroyer(Ship):
    def __init__(self):
        super().__init__(size=2)
```
---

## Dizaino stilius

Kode naudojamas **Factory pattern** stilius. Sukuriamas objektas (**Carrier**, **Battleship** ir kt.) pagal nurodytą tipą. Vartotojui nereikia tiesiogiai kviesti konstruktorių (`Carrier()`), užtenka `ShipFactory.create_ship("Carrier")`. Jei reikės pridėti naują laivo tipą, pakanka papildyti `ShipFactory`, o ne keisti visą kodą.

```python
class ShipFactory:
    @staticmethod
    def create_ship(ship_type):
        if ship_type == 'Carrier':
            return Carrier()
        elif ship_type == 'Battleship':
            return Battleship()
        elif ship_type == 'Cruiser':
            return Cruiser()
        elif ship_type == 'Submarine':
            return Submarine()
        elif ship_type == 'Destroyer':
            return Destroyer()
        else:
            raise ValueError(f"Unknown ship type: {ship_type}")
```

---

## Kompozicija

Šios sudėtinės `GUI` dalys kaip `cpu_grid`, `player_grid` negali veikti be `GUI` klasės, jei klasė būtų sunaikinta, žaidimas neveiktų.

```python
class GUI:
    def __init__(self, grid_file, winner_file):
        self.grid_file = grid_file
        self.winner_file = winner_file
        self.grid_size = self.read_grid_size()
        self.player_grid = [['•' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.cpu_grid = [['•' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        ship_type = ['Carrier', 'Battleship', 'Cruiser', 'Submarine', 'Destroyer',]
        self.player_ships = [ShipFactory.create_ship(st) for st in ship_type]
        self.cpu_ships = [ShipFactory.create_ship(st) for st in ship_type]
        self.player_hits = 0
        self.cpu_hits = 0
        self.root = tk.Tk()
        self.root.iconbitmap("krok.ico")
        self.root.title("Croca croca")
        self.enemy_buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player_buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.setup_game()
```

---

# Rezultatai

- Sukurtas pilnai veikiantis žaidimas  
- Implementuotos visos pagrindinės žaidimo mechanikos  
- Rezultatų sekimui faile rašomi laimėjimai  
- Sukurtas GUI

---

# Iššūkiai

- Sukurti GUI reikėjo `tkinter` bibliotekos, išmokti jos sintaksę  
- Laivų statymo algoritmą reikėjo parašyti taip, kad laivai nebūtų padėti vienas ant kito

---

# Išvada

Darbas atitinka visus reikalavimus ir yra tinkamas naudojimui. Objektinis programavimo stilius leidžia lengvai kodą plėsti ir tobulinti.

---

# Patobulinimai ateičiai

- Padaryti sunkumo lygius  
- Implementuoti kelių žaidėjų funkciją  
- Sukurti patrauklesnį programos dizainą, su garsais ir animacijomis  
- Leisti žaidėjui pačiam statyti laivus
