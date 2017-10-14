
import { Component } from '@angular/core';

import { User } from 'auth/auth.models';
import { UserService } from 'auth/user.service';
import { Game, GameStatus } from 'game/game.models';
import { GameManagerService } from 'game/manager/manager.service';


@Component({
    selector: 'app-root',
    templateUrl: './manager.component.html',
    styleUrls: ['./manager.component.css']
})
export class GameManagerComponent {
    currentUser: User;
    currentGame: Game;

    constructor(
        private userService: UserService,
        private gameManagerService: GameManagerService
    ) {
        userService.updateCurrentUser();
        userService.currentUser.subscribe((user) => {
            this.currentUser = user;
            gameManagerService.loadGames(GameStatus.NEW, user.username);
        });
    }
}
