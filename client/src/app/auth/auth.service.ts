
import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { JwtHelperService } from '@auth0/angular-jwt';
import { tap } from 'rxjs/operators';

import { SETTINGS } from '../settings/base';
import { BACKEND_URLS } from '../settings/routes';


@Injectable()
export class AuthService {
    private token;
    private storage;

    constructor(
        @Inject(SETTINGS) private settings,
        @Inject(BACKEND_URLS) private backendURLs,
        private http: HttpClient)
    {
        this.storage = window.localStorage;
    }

    isAuthenticated() {
        return new JwtHelperService().isTokenExpired();
    }

    login(username, password) {
        const loginUrl = `${this.backendURLs.apiBase}/${this.backendURLs.auth.login}`;

        const doLogin = (response) => {
            this.token = response.json().token;
            this.storage.setItem(this.settings.authTokenName, this.token);

            return true;
        }

        return this.http.post(loginUrl, {username, password}).pipe(tap(doLogin));
    }

    logout() {
        this.storage.removeItem(this.settings.authTokenName);
    }

}
