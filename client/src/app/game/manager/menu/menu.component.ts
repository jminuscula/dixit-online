
import { Component, Input } from '@angular/core';
import { Observable } from 'rxjs';
import { filter } from 'rxjs/operators';

import { User } from 'auth/auth.models';
import { UserService } from 'auth/user.service';
import { Game } from 'game/game.models';
import { GameManagerService } from 'game/manager/manager.service';


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
        private gameManagerService: GameManagerService
    ) {
        userService.currentUser.subscribe((user) => {
            this.user = user;
        });

        this.playableGames = gameManagerService.playableGames;
    }
}
