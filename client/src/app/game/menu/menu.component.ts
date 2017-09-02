
import { Component, Input } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { User } from '../../auth/auth.models';
import { Game } from '../game.models';


@Component({
    selector: 'menu',
    templateUrl: './menu.component.html',
})
export class MenuComponent {
    @Input() user: User;
    @Input() game: Game;
    @Input() userGames: Game[];

    constructor() {

    }
}
