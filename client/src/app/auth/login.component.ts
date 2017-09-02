
import { Component, OnInit, Inject } from '@angular/core';
import { Router } from '@angular/router';

import { URLS } from '../settings/routes';
import { AuthService } from './auth.service';


@Component({
    selector: 'login',
    templateUrl: './login.component.html',
})
export class LoginComponent {
    private auth;

    constructor(
        private router: Router,
        @Inject(URLS) private urls,
        private authService: AuthService,
    ) {
        this.auth = {};
    }

    isLoggedIn() {
        return this.authService.isAuthenticated();
    }

    onLogin() {
        this.router.navigate([this.urls.home]);
    }

    login(form) {
        if (this.authService.isAuthenticated()) {
            console.log('already authenticated');
            return this;
        }

        const setLoginError = () => {
            form.control.setErrors({
                invalidLogin: true
            });
        }

        this.authService.login(this.auth.username, this.auth.password)
            .subscribe(
                data => this.onLogin(),
                error => setLoginError()
            );
    }

};


@Component({
    template: '',
})
export class LogoutComponent implements OnInit {

    constructor(
        @Inject(URLS) private urls,
        private authService: AuthService,
        private router: Router
    ) {}

    ngOnInit() {
        this.authService.logout();
        this.router.navigate([this.urls.auth.login]);
    }

}
