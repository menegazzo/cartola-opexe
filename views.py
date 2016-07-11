# encoding: UTF-8
import math

from flask import jsonify
from flask.views import MethodView
import requests

import config


class TeamsAPIView(MethodView):

    def _get_league_info(self, page=1):
        return requests.get(
            'https://api.cartolafc.globo.com/auth/liga/opexe-xampios-legue?page={}'.format(page),
            headers={'X-GLB-Token': config.GLB_TOKEN}
        ).json()

    def get(self, slug):
        result = self._get_league_info()
        league = result['liga']
        team_total = league['total_times_liga']
        total_pages = int(math.ceil(team_total / (config.ITEMS_PER_PAGE * 1.0)))

        teams = result['times']
        if total_pages > 1:
            for i in xrange(2, total_pages + 1):
                result = self._get_league_info(page=i)
                teams += result['times']

        return jsonify(teams)


class PartialsAPIView(MethodView):

    def get(self, slug):
        team = requests.get('https://api.cartolafc.globo.com/time/{}'.format(slug))
        team = team.json()

        players = team['atletas']
        players = [player['atleta_id'] for player in players]

        partials = requests.get('https://api.cartolafc.globo.com/atletas/pontuados')
        partials = partials.json()
        partials = partials['atletas']
        partials = map(
            lambda player_id: partials.get(str(player_id), {}).get('pontuacao'),
            players,
        )

        total = sum(filter(lambda x: x or 0, partials))

        result = dict(zip(players, partials))
        result['total'] = total

        return jsonify(result)
