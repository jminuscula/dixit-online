
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from dixit.api.views import game as game_views
from dixit.api.views import player as player_views
from dixit.api.views import round as round_views


urlpatterns = [
    url(r'^game/$',
        game_views.GameList.as_view(), name='game-list'),
    url(r'^game/(?P<game_pk>[0-9]+)/$',
        game_views.GameRetrieve.as_view(), name='game-detail'),

    url(r'^game/(?P<game_pk>[0-9]+)/player/$',
        player_views.PlayerList.as_view(), name='player-list'),
    url(r'^game/(?P<game_pk>[0-9]+)/player/(?P<player_number>[0-9]+)/$',
        player_views.PlayerRetrieve.as_view(), name='player-detail'),

    url(r'^game/(?P<game_pk>[0-9]+)/round$',
        round_views.RoundList.as_view(), name='round-list'),
    url(r'^game/(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)$',
        round_views.RoundRetrieve.as_view(), name='round-detail'),
    url(r'^game/(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)/play$',
        round_views.PlayList.as_view(), name='play-list'),
    url(r'^game/(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)/provide$',
        round_views.PlayProvideCreate.as_view(), name='play-provide'),
    url(r'^game/(?P<game_pk>[0-9]+)/round/(?P<round_number>[0-9]+)/vote$',
        round_views.PlayVoteCreate.as_view(), name='play-vote'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
