# encoding: UTF-8
"""
# status do mercado
https://api.cartolafc.globo.com/mercado/status

# lista dos jogadores mais escalados
https://api.cartolafc.globo.com/mercado/destaques

# lista de patrocinadores
https://api.cartolafc.globo.com/patrocinadores

# lista das rodadas do campeonato (1 até 38)
https://api.cartolafc.globo.com/rodadas

# próximas partidas do campeonato
https://api.cartolafc.globo.com/partidas

# lista de clubes
https://api.cartolafc.globo.com/clubes

# lista de todos os jogadores (retorna todas as informações)
https://api.cartolafc.globo.com/atletas/mercado

# pontuação da rodada em andamento
https://api.cartolafc.globo.com/atletas/pontuados

# time que mais pontuou na rodada anterior
https://api.cartolafc.globo.com/pos-rodada/destaques

# busca geral de times, vai retornar info do time e o slug
https://api.cartolafc.globo.com/times?q=[nome do time]

# busca informações de um time específico, usar o slug do time.
https://api.cartolafc.globo.com/time/[slug do time]

# busca geral de ligas, para consultar uma liga específica é necessário token
https://api.cartolafc.globo.com/ligas?q=[nome da liga]

# busca informações de uma liga específica, usar o slug da liga.
https://api.cartolafc.globo.com/auth/liga/[slug da liga]
"""
# from __future__ import unicode_literals

import requests
from tinydb import TinyDB
from tinydb.queries import Query, where
from tinydb.storages import MemoryStorage

GLB_TOKEN = '18fe1197454aba1687c60129ec3e911537069664f5775355a767a4f65754367316e3943375a4a6848577a6a474970304a49734b784331776c5774595a6932597144567862336f646969465079553066393a303a6d656e6567617a7a6f40676d61696c2e636f6d'

status = requests.get('https://api.cartolafc.globo.com/mercado/status')
print status.json()

league = requests.get(
    'https://api.cartolafc.globo.com/auth/liga/opexe-xampios-legue',
    headers={'X-GLB-Token': GLB_TOKEN},
)
print league.json()

teams = requests.get('https://api.cartolafc.globo.com/time/menegazzo-e-c')
print teams.json()

partials = requests.get('https://api.cartolafc.globo.com/atletas/pontuados')
print partials.json()

response = requests.get('https://api.cartolafc.globo.com/atletas/mercado')
result = response.json()

db = TinyDB(storage=MemoryStorage)
for table_name, table_data in result.iteritems():

    if isinstance(table_data, dict):
        table_data = [value for value in table_data.itervalues()]
        table_data.sort(key=lambda x: x['id'])

    table = db.table(table_name)
    table.insert_multiple(table_data)

teams = db.table('clubes')
positions = db.table('posicoes')
status = db.table('status')
players = db.table('atletas')

# Getting best options for offensive players.
offensive = positions.get(where('nome') == 'Atacante')
probable = status.get(Query().nome == 'Provável')
probable_offensive_players = players.search((Query().posicao_id == offensive['id']) & (Query().status_id == probable['id']))
print len(probable_offensive_players)
#
# player = players.get(Query().apelido == 'Joel')
# for i, j in player.iteritems():
#     print i, j
