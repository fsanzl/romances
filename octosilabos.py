#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sys import argv

entrada = argv[1]
basename = entrada.split('.')[0]
octosilabos = pd.DataFrame()
df = pd.read_csv(entrada)

df['Rima'] = df['Rima'].str.replace('-','')
df['Consonancia'] = df['Consonancia'].replace('-','')
titulo = df.at[3, 'Pieza']
autor = df.at[3, 'Autor']
nversos = {'NVersos': len(df.index)}
basename = f'{autor}_{titulo}'
dfo = df[df['Slbs'] == 8]


for indice, fila in dfo.iterrows():
    fila = {'Autor':autor, 'Obra': titulo, 'Ritmo': fila['Ritmo']}
    octosilabos = octosilabos.append(fila, ignore_index=True)
octosilabos.to_csv(f'{autor}_{titulo}_octosilabos.csv', index=False)




