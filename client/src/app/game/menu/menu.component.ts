
import { Component, Input } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/filter';

import { User } from '../../auth/auth.models';
import { UserService } from '../../auth/user.service';
import { Game } from '../game.models';
import { GameService } from '../game.service';


@Component({
    selector: 'menu',
    templateUrl: './menu.component.html',
})
export class MenuComponent {
    @Input() currentGame: Game;

    private user: User;
    private playableGames: Observable<Game[]>;

    constructor(
        private userService: UserService,
        private gameService: GameService
    ) {
        userService.currentUser.subscribe((user) => {
            this.user = user;
        });

        this.playableGames = gameService.playableGames;
    }

    selectGame(game) {
        this.gameService.selectGame(game);
    }
}
