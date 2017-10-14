
import { Component, Inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router }   from '@angular/router';

import { URLS } from 'settings/routes';
import { Game } from 'game/game.models';
import { GameManagerService } from 'game/manager/manager.service';


@Component({
    template: `
        debug game screen {{ game | json }}
    `,
})
export class DebugScreen implements OnInit {
    game: Game;

    constructor(
        private gameManagerService: GameManagerService,
        @Inject(URLS) private urls,
        private route: ActivatedRoute,
        private router: Router
    ) { }

    ngOnInit() {
        this.route.params.subscribe(p => (this.getGame(p && p.gameId)));
    }

    getGame(gameId) {
        const setGame = (game) => {
            if (!game) {
                return this.router.navigate([this.urls.home]);
            }

            this.game = game;
        };

        this.gameManagerService.getGame(gameId).subscribe(setGame);
    }
}
