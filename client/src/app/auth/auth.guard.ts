
import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';

import { AuthService } from './auth.service';


@Injectable()
export class IsAuthenticatedGuard implements CanActivate {

    constructor(private authService: AuthService, private router: Router) {}

    canActivate() {
        const loggedIn = this.authService.isAuthenticated();
        if (!loggedIn) {
            this.router.navigate(['/login']);
            return false;
        }

        return true;
    }

}
