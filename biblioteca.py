def carica_da_file(file_path):
    biblioteca={}
    titolo = []
    autore = []
    anno=[]
    pagine=[]
    sezione = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line=line.strip().split(";")
                if not line:
                    continue
                titolo=line[0]
                autore = line[1]
                anno = line [2]
                pagine = line[3]
                sezione = line[4]
                if sezione not in biblioteca:
                    biblioteca[sezione] = []
                biblioteca[sezione].append({"titolo": titolo.strip(),"autore": autore.strip(),"anno": anno.strip(),"pagine": pagine.strip()})
            return biblioteca
    except FileNotFoundError:
        return None



def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    libro=[titolo, autore, anno, pagine, sezione]
    if libro not in biblioteca:
        with open(file_path, "a", encoding="utf-8") as file:
            biblioteca[sezione].append({"titolo": titolo.strip(), "autore": autore.strip(), "anno": anno.strip(), "pagine": pagine.strip()})
    else:
        libro=None
    return libro



def cerca_libro(biblioteca, titolo):
    libro=None
    for line in biblioteca:
        line=line.strip.split
        if line[0]==titolo:
            libro=line
    return libro


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    lista=[]
    for line in biblioteca:
        line=line.strip.split
        if line[4]==sezione:
            lista.append(line)
    lista.sort()
    return lista



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

