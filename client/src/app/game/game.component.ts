
import { Component } from '@angular/core';

import { User } from '../auth/auth.models';
import { UserService } from '../auth/user.service';
import { Game, GameStatus } from './game.models';
import { GameService } from './game.service';


@Component({
    selector: 'app-root',
    templateUrl: './game.component.html',
    styleUrls: ['./game.component.css']
})
export class GameComponent {
    currentUser: User;
    currentGame: Game;

    constructor(
        private userService: UserService,
        private gameService: GameService
    ) {
        userService.updateUserInfo();
        userService.userInfo.subscribe((user) => {
            this.currentUser = user;
            gameService.loadGames(GameStatus.NEW, user.username);
        });

        gameService.currentGame.subscribe((game) => {
            this.currentGame = game;
        });
    }
}
