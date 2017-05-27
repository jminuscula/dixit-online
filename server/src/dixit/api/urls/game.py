
from django.conf.urls import url

from dixit.api.views.game import game
from dixit.api.views.game import player
from dixit.api.views.game import round


urlpatterns = [
    url(r'^$',
        game.GameList.as_view(), name='game-list'),
    url(r'^(?P<game_pk>[0-9]+)/$',
        game.GameRetrieve.as_view(), name='game-detail'),

    url(r'^(?P<game_pk>[0-9]+)/player/$',
        player.PlayerList.as_view(), name='player-list'),
    url(r'^(?P<game_pk>[0-9]+)/player/(?P<player_number>[0-9]+)/$',
        player.PlayerRetrieve.as_view(), name='player-detail'),

    url(r'^(?P<game_pk>[0-9]+)/round$',
        round.RoundList.as_view(), name='round-list'),
    url(r'^(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)$',
        round.RoundRetrieve.as_view(), name='round-detail'),
    url(r'^(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)/play$',
        round.PlayList.as_view(), name='play-list'),
    url(r'^(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)/provide$',
        round.PlayProvideCreate.as_view(), name='play-provide'),
    url(r'^(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)/vote$',
        round.PlayVoteCreate.as_view(), name='play-vote'),

]
