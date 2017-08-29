
import { Component } from '@angular/core';

import { User } from '../auth/auth.models';
import { UserService } from '../auth/user.service';


@Component({
    selector: 'app-root',
    templateUrl: './game.component.html',
    styleUrls: ['./game.component.css']
})
export class GameComponent {
    title = 'dixit!';
    currentUser: User;

    constructor(private userService: UserService) {
        userService.updateUserInfo();

        userService.userInfo.subscribe((user) => {
            this.currentUser = user;
        });
    }
}
