# Auto spotted

> Automatyczne spotted
>
> ### Spis treści
>
> * [Czym jest Auto spotted?](#about)
> * [Opis działania](#dzialanie)
> * [Zastosowane technologie](#technologie)
> * [Konfiguracja i uruchomienie](#konfiguracja)

## Czym jest Auto spotted?<a id="about"></a>

To nic innego jak zautomatyzowana wersja klasycznego spotted. Znacząco jednak różni się od 'normalnej' wersji - jest w
pełni automatyczne i działa asynchronicznie, do działania nie potrzebuje osoby, która robi screeny wpisów i wrzuca je na
Instagram.

## Opis działania<a id="dzialanie"></a>

Po kliknięciu znajdującego się na Instagramie linku do spotted (czy też adresu IP serwera, cięcie kosztów), otwiera nam
się strona internetowa aplikacji, która wygląda tak:

![image](docs/home_page.png)

Po wpisaniu wiadomości i naciśnięciu przycisku ***wyślij***, pojawia się komunikat o tym, że wiadomość jest
przetwarzana. Po wyłączeniu komunikatu i odczekaniu kilku sekund, strona przekierowuje na Instagrama, gdzie już można
znaleźć wysłaną przez siebie wiadomość. W przypadku pojawienia się błędu, strona wyświetli komunikat o błędzie i jego
opisie.

Każda wysłana wiadomość na stronie trafia również na adres email administratora, dzięki czemu ma on od razu wgląd do
błędu, lub treści publikacji.

*Przykładowy email o pomyślnym dodaniu posta*

![image](docs/successfully_added.png)

*Przykładowy email o błędzie podczas publikacji posta*

![image](docs/error.png)

## Zastosowane technologie <a id="technologie"></a>

Aplikacja została postawiona na darmowym wirtualnym serwerze w usłudze Oracle Cloud, na którym zainstalowano **Apache2**
oraz **Python 3.10**.

Backend aplikacji działa na zasadzie *REST API*.

Po wpisaniu wiadomości na stronie i wciśnięciu przycisku, wykonuje się zapytanie (***fetch***) metodą *POST* na *
*backend**, który odbiera i przetwarza wysłaną wiadomość.

> ```javascript
> const response = await fetch(
>     "http://130.61.254.123:8000/",
>     {
>          method: "POST",
>          mode: "cors",
>          headers: {
>              "Access-Control-Request-Method": "POST",
>              "accept": "application/json",
>              "Access-Control-Request-Headers": ["Content-Type", "Authorization"],
>              "Content-Type": "application/json"
>          },
>          body: JSON.stringify({"message": dataToSend})
>      }
>      )
>      return response.json()
> ```
>
> *Fragment funkcji z pliku [index.html](pages/index.html)*

API stworzone jest przy użyciu webowego frameworka ***FastAPI*** w języku Python. Otrzymane od frontendu wiadomości są
na początku sprawdzane pod względem wulgaryzmów - jeżeli jakiś się pojawi, backend zwraca o tym informację do strony i
post się nie publikuje. Lista wulgaryzmów, które są sprawdzane, dostępna jest [tutaj](app/banned_words.txt).

> ```python
> with open("banned_words.txt", "r") as f:
>             for line in f.readlines():
>                 if line.strip() in body["message"]:
>                     return {
>                         "status_code": 451,
>                         "message": "Unavailable For Legal Reasons"
>                     }
> ```
>
> *Fragment funkcji z pliku [api.py](app/api.py)*

Następnym krokiem jest zamiana tekstu na zdjęcie, do którego wykorzystywany jest moduł Pillow oraz pilmoji, dzięki
którym możliwe jest wstawienie tekstu do zdjęcia z tłem.

> ```python
> img = Image.open(f"{os.getcwd()}/images/base.png")
> font = ImageFont.truetype(f"{os.getcwd()}/fonts/NotoSansNandinagari-Regular.ttf", 50, encoding='utf-8')
> draw_multiple_line_text(img, text, font, (255, 255, 255), 120)
> img.save(f"{os.getcwd()}/images/image{posts_count}.png")
> ```
>
> *Fragment funkcji z pliku [image.py](app/image.py)*

Gotowe zdjęcie jednak nie może zostać wysłane od razu na Instagrama - do publikacji potrzebny jest adres url do zdjęcia,
a nie sam plik. Dlatego też zdjęcia wysyłane są za pomocą zapytania POST do API serwisu Imgur, który umożliwia
przesyłanie zdjęć w formie bitów, zwracając link.

> ```python
> def upload_image(image):
>     url = "https://api.imgur.com/3/image"
>     headers = {
>         "Authorization": f"Client-ID {os.getenv('IMGUR_CLIENT_ID')}"
>     }
>     payload = {
>         "image": image
>     }
>     files = []
>     response = requests.request("POST", url, headers=headers, data=payload, files=files)
>     return response.json()['data']['link']
> ```
>
> *Fragment kodu z pliku [image.py](app/image.py)*

Otrzymany z powyższej funkcji adres url, przesyłany jest, również za pomocą zapytania POST, do API Instagrama, na którym
już przebiega końcowa część publikacji zdjęcia.

> *Funkcje z zapytaniami do API Instagrama dostępne w pliku [publish.py](app/publish.py)*

## Konfiguracja i uruchomienie <a id="konfiguracja"></a>

#### Zmienne środowiskowe

Aby poprawnie uruchomić aplikację, należy na początku uzupełnić zmienne środowiskowe. Powinny one znajdować się w pliku
***.env*** w głównym katalogu projektu.

Do szybszego stworzenia pliku można wykorzystać plik [.env.example](.env.example).

```shell
cp .env.example .env
```

Opis poszczególnych zmiennych środowiskowych

| **Nazwa**            | **Opis**                                                                                                                                            | **Wartość domyślna**        |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| INSTAGRAM_ACCOUNT_ID | ID konta Instagram połączonego z aplikacją                                                                                                          |                             |
| ACCESS_TOKEN         | Token dostępu do aplikacji z uprawnieniami do zarządzania treścią ([link do wygenerowania tokenu](https://developers.facebook.com/tools/explorer/)) |                             |
| IMAGE_KIT_PRIVATE    | ID konta na platformie ImageKit (do publikacji zdjęć, by dostać adres url)                                                                          |                             |
| IMAGE_KIT_PUBLIC     | Hasło do konta na platformie ImageKit                                                                                                               |                             |
| IMAGE_KIT_ENDPOINT   | Endpoint URL do konta na platformie Imgur                                                                                                           |                             |
| SMTP_PORT            | Port serwera SMTP                                                                                                                                   | 465                         |
| SMTP_PASSWORD        | Hasło do konta, z którego wysyłane są maile do administratora                                                                                       |                             |
| SMTP_MAIL            | Mail konta, z którego wysyłane są maile do administratora                                                                                           | auto.spotted.zset@gmail.com |
| ADMIN_MAIL           | Mail konta administratora                                                                                                                           |                             |

Po uzupełnieniu wszystkich zmiennych w pliku ***.env***, należy zainstalować na serwerze usługi Apache2 oraz Python3.10,
a następnie wszystkie biblioteki Pythona, które dostępne są w pliku [requirements.txt](requirements.txt).

Można zrobić to za pomocą komendy:

```shell
python3.10 -m pip install -r requirements.txt
```

Gdy moduły zostaną zainstalowane, można uruchomić backend - przechodząc najpierw do katalogu ***/app***, a następnie
uruchamiając plik [api.py](app/api.py) wpisując komendę:

```shell
python3.10 api.py
```

Jeżeli aplikacja działa, należy edytować plik [index.html](pages/index.html) i w linijce numer 130 zmienić adres IP na
adres IP, na którym działa backend. Po tej zmianie można uruchomić usługę
Apache2 ([poradnik](https://soisk.info/index.php/Linux_Ubuntu_-_Instalacja_i_konfiguracja_serwera_Apache2)).

Po prawidłowej konfiguracji strona powinna mieć możliwość komunikacji z backendem, a dzięki temu powinna poprawnie
działać.
