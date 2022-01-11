#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sys import argv

entrada = argv[1]
basename = entrada.split('.')[0]

df = pd.read_csv(entrada)

df['Rima'] = df['Rima'].str.replace('-', '')
df['Consonancia'] = df['Consonancia'].replace('-', '')
dfo = df[df['Slbs'] == 8]
nversos = 0
titulo = df.at[3, 'Pieza']
autor = df.at[3, 'Autor']
octosilabos = {'Octosílabos': len(df[df['Slbs'] == 8].index)}
nversos = {'NVersos': len(df.index)}

basename = f'{autor}_{titulo}'
ristra = []
ristras = []
def nversos(estrofa):
    return len(estrofa) > 5
for indice, fila in dfo.iterrows():
    if len(ristra) < 1:
        ristra.append((fila['Verso'], fila['Rima'],
                       fila['Consonancia'], fila['Ritmo']))
    elif fila['Verso'] == ristra[-1][0] + 1:
        ristra.append((fila['Verso'], fila['Rima'],
                       fila['Consonancia'], fila['Ritmo']))
        if len(dfo) == indice + 1 and nversos(ristra):
            ristras.append(ristra)
    else:
        if nversos(ristra):
            ristras.append(ristra)
        ristra = [(fila['Verso'], fila['Rima'],
                   fila['Consonancia'], fila['Ritmo'])]
def rimas(estrofa):
    idx = [i for i in range(len(estrofa)) if i % 2 == 1]
    return not all(linea[2] == estrofa[1][2] for
        linea in estrofa[1::2])

def redondilla(estrofa):
    if len(estrofa) >3:
        if estrofa[-1][2] == estrofa[-4][2] and estrofa[-2][1] == estrofa[-3][1]:
            estrofa = redondilla(estrofa[:-4])
    return estrofa

romances = []
romance = []
redondillas = []
for ristra in ristras:
    if nversos(romance) and rimas(romance):
        romances.append(romance)
    romance = []
    for verso in ristra:
        if len(romance) % 2 == 0 or len(romance) < 2 or (
            verso[1] == romance[-2][1]):
            romance.append(verso)
            romance = redondilla(romance)
        elif len(romance) == 3:
            romance = romance[1:] + [verso]
        else:
            if rimas(romance) and nversos(romance):
                romances.append(romance[:-1])
            romance = [romance[-1], verso]
if nversos(romance) and rimas(romance):
    romances.append(romance)

conta = 1
df = pd.DataFrame()
for romance in romances:
    for verso in romance:
        fila = {'Autor': autor, 'Obra': titulo,
                'n': conta, 'Romance': romance[1][1],
                'Verso': verso[0], 'Rima': verso[1],
                'Consonancia': verso[2], 'Ritmo': verso[3]}
        df = df.append(fila, ignore_index=True)
    conta += 1
df.convert_dtypes().to_csv(f'{autor}_{titulo}_romances.csv', index=False)
