
import { Component, OnInit} from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from './auth.service';


@Component({
    selector: 'login',
    templateUrl: './login.component.html',
})
export class LoginComponent {
    private auth;

    constructor(private authService: AuthService, private router: Router) {
        this.auth = {};
    }

    isLoggedIn() {
        return this.authService.isAuthenticated();
    }

    onLogin() {
        this.router.navigate(['']);
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

    constructor(private authService: AuthService, private router: Router) {}

    ngOnInit() {
        this.authService.logout();
        this.router.navigate(['login']);
    }

}
