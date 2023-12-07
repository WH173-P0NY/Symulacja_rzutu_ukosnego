# Symulacja_rzutu_ukosnego
Symulator Rzutu Ukośnego
Opis
Aplikacja "Symulator Rzutu Ukośnego" to narzędzie służące do wizualizacji trajektorii rzutu ukośnego. Użytkownik może wprowadzić parametry początkowe rzutu, takie jak prędkość początkową, kąt wyrzutu oraz położenie początkowe, a aplikacja wyświetla symulowaną trajektorię ruchu.

Funkcjonalności
Wprowadzanie parametrów rzutu (prędkość początkowa, kąt wyrzutu, położenie początkowe).
Wizualizacja trajektorii rzutu.
Możliwość zatrzymania i zresetowania symulacji.
Wyświetlanie składowych prędkości w różnych punktach trajektorii.
Instrukcja Użycia
Aby uruchomić symulator, użytkownik powinien:

Wprowadzić prędkość początkową, kąt wyrzutu oraz położenie początkowe w odpowiednich polach.
Kliknąć przycisk "Start" aby rozpocząć symulację.
Użyć przycisków "Stop" i "Reset", aby zatrzymać lub zresetować symulację.
Struktura Projektu
Projekt jest dostępny w dwóch wersjach:

Wersja Jednoplikowa: Cała logika i interfejs użytkownika znajdują się w jednym pliku bez_importu.py.
Wersja Modułowa: Projekt podzielony jest na trzy pliki:
main.py: Główny plik, uruchamiający aplikację.
logic_for_rzut.py: Zawiera logikę obliczeniową symulacji.
UI_for_rzut.py: Zawiera definicję interfejsu użytkownika.
W zależności od preferencji, użytkownik może wybrać wersję jednoplikową dla prostoty, lub wersję modułową dla lepszej organizacji kodu i łatwiejszego utrzymania.

Wymagania
Aplikacja wymaga Pythona w wersji 3.x oraz bibliotek numpy, matplotlib i tkinter.
