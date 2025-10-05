def carica_da_file(file_path):
    biblioteca={}       # Crea un dizionario vuoto che conterrà le sezioni come chiavi e liste di libri come valori
    try:
        with open(file_path, "r", encoding="utf-8") as file:        # Apre il file in modalità lettura con codifica UTF-8
            for line in file:           # Scorre ogni riga del file
                line=line.strip()       # Rimuove spazi bianchi iniziali/finali e il carattere di newline
                if not line:
                    continue            # Se la riga è vuota, salta alla successiva
                parti=line.split(",")   # Divide la riga in parti usando la virgola come separatore
                if len(parti) != 5:
                    continue            # Se la riga non ha esattamente 5 campi, la ignora per evitare problemi se il file presentasse errori all'interno
                titolo, autore, anno, pagine, sezione = [p.strip() for p in parti]      #Assegnazione di valori alle variabili (è presente un ulteriore strip per rimuovere eventuali spazi ancora presenti)
                try:
                    anno = int(anno)
                except ValueError:      # Tenta di convertire l'anno in intero, altrimenti lascia il valore originale
                    anno = anno
                try:
                    pagine = int(pagine)
                except ValueError:      # Tenta di convertire il numero di pagine in intero, altrimenti lascia il valore originale
                    pagine = pagine
                if sezione not in biblioteca:
                    biblioteca[sezione] = []    # Se la sezione non esiste nel dizionario, la inizializza con una lista vuota
                biblioteca[sezione].append({"titolo": titolo,"autore": autore,"anno": anno,"pagine": pagine})       # Aggiunge il libro (come dizionario) alla lista della sezione
            return biblioteca       # Restituisce l'intera struttura dati al termine della lettura
    except FileNotFoundError:
        return None                 # Se il file non esiste, restituisce None per indicare errore



def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    if sezione not in biblioteca:
        biblioteca[sezione] = []            # Se la sezione non esiste ancora, la crea
    for libro in biblioteca[sezione]:
        if libro["titolo"].lower() == titolo.lower() and libro["autore"].lower() == autore.lower():         # Controlla se il libro (stesso titolo e autore, senza considerare maiuscole/minuscole) è già presente
            return None         # Se duplicato, non aggiunge e ritorna None come indicatore
    try:                        # Tenta di convertire anno e pagine in interi; in caso di errore mantiene il valore originale
        anno = int(anno)
    except (ValueError, TypeError):
        anno = anno
    try:
        pagine = int(pagine)
    except (ValueError, TypeError):
        pagine = pagine
    nuovo = {"titolo": titolo, "autore": autore, "anno": anno, "pagine": pagine}        # Crea il dizionario che rappresenta il nuovo libro
    biblioteca[sezione].append(nuovo)                                                   # Lo aggiunge alla lista della sezione
    try:
        with open(file_path, "a", encoding="utf-8") as file:        # Apre il file in modalità append e scrive i dati del nuovo libro
            file.write(f"{titolo};{autore};{anno};{pagine};{sezione}\n")        # Se c'è un errore di scrittura, rimuove il libro appena aggiunto dalla struttura dati
    except Exception as e:
        biblioteca[sezione].remove(nuovo)
        print("Errore scrittura file:", e)
        return None
    return nuovo                   # Se tutto OK, restituisce il dizionario del libro appena aggiunto

def cerca_libro(biblioteca, titolo):
    titolo=titolo.lower()           # Normalizza il titolo in minuscolo per ricerche case-insensitive
    for sezione, libri in biblioteca.items():       # Scorre tutte le sezioni e i libri
        for libro in libri:
            if libro["titolo"].lower() == titolo:   # Confronta i titoli normalizzati
                risultato = libro.copy()
                risultato["sezione"] = sezione
                return risultato
    return None                     # Se non trova nulla, ritorna None


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    sezione = str(sezione)          # Assicura che la sezione sia una stringa
    if sezione not in biblioteca:
        return []                   # Se la sezione non esiste, ritorna lista vuota
    lista=[libro["titolo"] for libro in biblioteca[sezione]]        # Crea una lista dei soli titoli presenti nella sezione
    lista.sort()                    # Ordina alfabeticamente i titoli
    return lista                    # Restituisce la lista ordinata



def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

