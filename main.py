import math
import random
import easygui
import numpy as np
import copy


def generuj_wagi(struktura, min_waga, max_waga):
    index = -1
    wagi = []
    neurony = []
    warstwy = []
    for x in struktura:
        index+=1
        if index > 0:
            for y in range(x):
                for z in range(poprz+1):
                    wagi.append(random.uniform(int(min_waga), int(max_waga)))
                neurony.append({"wagi": wagi})
                wagi = []
            warstwy.append(neurony)
            neurony = []
        poprz = x
    return warstwy


def propagacja_wprzod(wejscie,warstwy,l_neurony, beta):
    n_wejscie = []
    for x in range(len(l_neurony)): #petla po warstwach
        n_wejscie.append(1)
        for y in warstwy[x]: #pętla po neuronach
            tab = list(y['wagi'])
            s_licz = np.multiply(tab, wejscie)
            s = sum(s_licz)
            y['s'] = s
            f_atywacji = 1 / (1 + math.exp(-float(beta) * s))
            y['wy'] = f_atywacji
            n_wejscie.append(f_atywacji)
            y['we'] = wejscie
        wejscie = n_wejscie
        n_wejscie = []
    return warstwy


def oblicz_korekte(warstwy, wart_uczenia, oczekiwana):
    index = -1
    for x in warstwy[0]:
        index += 1
        if len(oczekiwana) ==1:
            blad = oczekiwana[0] - x['wy']
        else:
            blad = oczekiwana[index] - x['wy']
        x['blad'] = blad
        korekta = float(wart_uczenia) * blad
        x['korekta'] = korekta

    return warstwy


def wsteczna_propagacja(warstwy,l_neurony,beta):
    korekty = []
    n_korekta = []

    #liczenie dla ostatniej
    for y in warstwy[0]:
        korekta = y["korekta"] * beta * y['wy'] * (1 - y['wy'])
        korekty.append(korekta)
        nowe_w = list(np.multiply(korekta, y['we']))
        y['nowe wagi'] = list(np.array(nowe_w) + np.array(y['wagi']))
    #liczenie dla następnych
    for x in range(1,len(l_neurony)):
        for z in warstwy[x]:
            for j in range(len(korekty)):
                nowe_s = korekty[j]* beta * z['wy'] * (1 - z['wy'])
                nowe_w = list(np.multiply(nowe_s, z['we']))
                if j > 0:
                    z['nowe wagi'] = list(np.array(nowe_w) + np.array(z['nowe wagi']))
                else:
                    z['nowe wagi'] = nowe_w
                n_korekta.append(nowe_s)
            z['nowe wagi'] = list(np.array(z['wagi']) + np.array(z['nowe wagi']))
            korekty = n_korekta

    return warstwy


def wyzeroj_wartosci_warstwy(l_neurony,warstwy):

    for x in range(0, len(l_neurony)):
        for y in warstwy[x]:
            y['wagi'] = y['nowe wagi']
            if 'korekta' in y.keys():
                del y['korekta']
            if 'blad' in y.keys():
                del y['blad']
            if 'nowe wagi' in y.keys():
                del y['nowe wagi']
            del y['s']
            del y ['wy']
            del y ['we']

    return warstwy


def naucz_sie(ilosc_epok, warstwy, l_neurony, beta, wart_uczenia,inputs,oczekiwana):
    for x in range(ilosc_epok):

        warstwy = propagacja_wprzod(inputs, warstwy, l_neurony, beta)

        warstwy.reverse()

        warstwy = oblicz_korekte(warstwy, wart_uczenia, oczekiwana)

        if x == ilosc_epok-1:
            obliczone = []
            for y in warstwy[0]:
                obliczone.append(y['wy'])
            return obliczone

        warstwy = wsteczna_propagacja(warstwy, l_neurony,beta)

        warstwy = wyzeroj_wartosci_warstwy(l_neurony, warstwy)

        warstwy.reverse()

def main():
    sciezka = easygui.fileopenbox()

    if 'XOR' in sciezka:
        inp = []
        out = []
        inpts = []
        outpts = []
        f = open(sciezka, "r")
        for line in f:
            line = line.rstrip('\n')
            inp.append(1) ###dodawanie antenki
            for x in range(2):
                inp.append(int(line[x]))
            inpts.append(inp)
            out.append(int(line[len(line)-1]))
            outpts.append(out)
            inp = []
            out = []

    if 'XOR+NOR' in sciezka:
        inp = []
        out = []
        inpts = []
        outpts = []
        f = open(sciezka, "r")
        for line in f:
            line = line.rstrip('\n')
            inp.append(1)
            for x in range(2):
                inp.append(int(line[x]))
            for y in range(2,4):
                out.append(int(line[y]))
            inpts.append(inp)
            outpts.append(out)
            inp = []
            out = []

    if 'SUMATOR' in sciezka:
        inp = []
        out = []
        inpts = []
        outpts = []
        f = open(sciezka, "r")
        for line in f:
            line = line.rstrip('\n')
            inp.append(1)
            for x in range(3):
                inp.append(int(line[x]))
            for y in range(3, 5):
                out.append(int(line[y]))
            inpts.append(inp)
            outpts.append(out)
            inp = []
            out = []

    struktura = list(map(int, input("podaj strukture(np. 3-2-2): ").split("-")))
    print("Podana struktura: ", struktura)

    min_waga, max_waga = input("Podaj przedział wag(po spacji): ").split()

    beta = float(input("Podaj wartość beta: "))
    wart_uczenia = float(input("Podaj wartosc uczenia: "))
    ilosc_epok = int(input("podaj liczbę epok: "))
    wejscia = struktura[0]
    wyjscia = struktura[len(struktura) - 1]

    l_neurony = copy.deepcopy(struktura)
    del l_neurony[0]

    warstwy_kopia = generuj_wagi(struktura,min_waga, max_waga)

    for x in range(len(inpts)):

        warstwy = copy.deepcopy(warstwy_kopia)

        wej = inpts[x]
        ocz = outpts[x]
        print()
        print(wej,ocz)
        print(naucz_sie(ilosc_epok,warstwy,l_neurony,beta,wart_uczenia,wej,ocz))

main()
exit()


