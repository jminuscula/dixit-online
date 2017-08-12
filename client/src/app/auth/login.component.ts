
import { Component } from '@angular/core';

import { AuthService } from './auth.service';


@Component({
    selector: 'login',
    templateUrl: './login.component.html',
})
export class LoginComponent {
    private loggedIn: boolean;

    constructor(private authService: AuthService) {}

    isLoggedIn() {
        return this.authService.isAuthenticated();
    }

    login() {
        if (this.authService.isAuthenticated()) {
            console.log('already authenticated');
            return this;
        }

        this.authService.login('player1', 'password')
            .then(success => console.log('success:', success));
    }

    logout() {
        this.authService.logout();
        console.log('logged out');
    }

};
