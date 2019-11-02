**Versions**
* Maven 3
* Java 8
* Lucene 6.6.0
* Tika 1.20

*Tika si Lucene sunt importate ca dependinte in pom.xml*

*Proiectul contine 3 clase*

1. **CustomRomanianAnalyzer** 

    Initial am incercat sa folosesc RomanianAnalyzer, dar am observat ca, by default,
    RomanianAnalyzer nu scapa de diacritice. Astfel, am creat un nou Analyzer in care
    am folosit StopWords din RomanianAnalyzer iar in "createComponents" am adaugat si
    filtrul ASCIIFoldingFilter care scapa de diacritice. Restul filtrelor sunt exact
    cele din RomanianAnalyzer intrucat sunt cele de care am avut nevoie si au fost
    doar completate

2. **Indexer**

    Aceasta clasa preia citeste, folosind Tika, toate fisierele din folderul dat ca 
    parametru ("inputDirectory"). Aceste fisiere citite sunt indexate si scrise in 
    folderul dat ca parametru in "indexDirectory". A fost necesar sa se foloseasca Tika
    intrucat cu un Scanner normal nu se pot citi fisiere de tipul ".docx" si ".pdf"
    intrucat acestea sunt criptate. 

3. **Search**

    Clasa search contine metoda main, si cea care trebuie rulata. Se face indexarea,
    se creeaza un searcher care se uita in folderul de indecsi, si se cer cuvinte de
    cautat care sunt cautate prin crearea unui query simplu care se uita in fisierele
    indexate. Se afiseaza numarul fisierelor in care apar rezultatele si fisierele
    in care au aparut

* **Input** 

    Ca default, am folosit folderul "resources" pentru a tine fisierele de citit si
    fisierele de indexare.

* **Probleme Intampinate**

    Am observat ca RomanianAnalyzer nu ia in considerare toate articolele hotarate
    existente in limba romana, nici in versiunea folosita, nici in ultima versiune
    (adica 8.0.0). Spre exemplu daca intr-un fisier am cuvantul "mama" si caut cuvantul
    "mamei" nu se va gasi acel fisier intrucat, in lista de articole (care este generata
    automat in libraria lucene) nu exista articolul "ei". Astfel, exista sansa ca unele 
    cuvinte sa nu fie gasite.
	