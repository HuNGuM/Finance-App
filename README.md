# Finance Manager

Finance Manager — to aplikacja desktopowa do zarządzania finansami osobistymi z możliwością ewidencjonowania dochodów, wydatków oraz generowania raportów.

## 🔧 Instalacja (klonowanie projektu)

1. Sklonuj repozytorium:
```bash
git clone https://github.com/your-username/finance-app.git
cd finance-app
```

2. Utwórz środowisko wirtualne i aktywuj je:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Uruchom aplikację:
```bash
python finance_app/main.py
```

## 🧰 Użyte technologie

- **Python 3.12**
- **Tkinter** — GUI
- **SQLite3** — база данных
- **FPDF** — генерация PDF-отчетов
- **Matplotlib** — круговые диаграммы
- **PyInstaller** — сборка `.exe`
- **pytest** — тестирование

## 🧪Przykłady funkcji i metod

### `Database.create_schema(self)`
- **Wejście:** nic  
- **Wyjście:** nic 
- **Przeznaczenie:** ładuje i wykonuje skrypt SQL `migrations.sql`,  tworząc tabele w bazie danych.

### `MainWindow.add_transaction(self)`
- **Wejście:** Odczytuje dane z pól interfejsu (kwota, kategoria, data, opis, konto)  
- **Wyjście:** nic
- **Przeznaczenie:** Dodaje transakcję do bazy danych i aktualizuje saldo konta.

### `MainWindow.show_report(self)`
- **Wejście:** Data początku i końca (określana przez filtr), typ transakcji, filtr według kategorii i konta
- **Wyjście:** Okno z wykresem kołowym
- **Przeznaczenie:** Pokazuje rozkład dochodów lub wydatków według kategorii.

### `TransactionRepository.get_by_type_and_period(...)`
- **Wejście:** Typ transakcji, data początku i końca, opcjonalne filtry: kategoria, ID konta
- **Wyjście:** lista `Transaction`  
- **Przeznaczenie:** Filtruje transakcje według typu i przedziału czasowego.

### `parse_pko_pdf(filepath: str) -> list[Transaction]`
- **Wejście:** Ścieżka do pliku PDF  
- **Wyjście:** lista obiektów `Transaction`  
- **Przeznaczenie:** Parsuje wyciąg bankowy PKO i przekształca dane w transakcje.

## 🧪 Testowanie

```bash
pytest
```
Testy znajdują się w katalogu tests/ i obejmują:
- repozytoria (`account_repo`, `transaction_repo`)
- logikę importu PDF
- logikę biznesową `report_service`
- interfejs (`main_window`)

## 📦 Tworzenie pliku`.exe`

```bash
pyinstaller --noconfirm --onefile --add-data "finance_app/db/migrations.sql;db" --add-data "finance_app/fonts/DejaVuSans.ttf;fonts" finance_app/main.py
```

Lub z `main.spec`:

```bash
pyinstaller main.spec
```

Plik `main.exe` będzie znajdować się w katalogu `finance_app/dist/`.