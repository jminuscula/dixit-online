
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router }   from '@angular/router';

import { Game } from 'game/game.models';
import { GameManagerService } from 'game/manager/manager.service';


@Component({
    template: `
        debug game screen {{ game?.id }}
    `,
})
export class DebugScreen implements OnInit {
    game: Game;

    constructor(
        private gameManagerService: GameManagerService,
        private route: ActivatedRoute,
        private router: Router) {

    }

    ngOnInit() {
        this.route.params.subscribe(p => (this.getGame(p && p.gameId)));
    }

    getGame(gameId) {
        const setGame = g => (this.game = g);
        this.gameManagerService.getGame(gameId).subscribe(setGame);
    }
}
