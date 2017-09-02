
import { Injectable, Inject } from '@angular/core';
import { Http } from '@angular/http';

import { tokenNotExpired } from 'angular2-jwt';
import 'rxjs/add/operator/map';

import { SETTINGS } from '../settings/base';
import { BACKEND_URLS } from '../settings/routes';


@Injectable()
export class AuthService {
    private token;
    private storage;

    constructor(
        @Inject(SETTINGS) private settings,
        @Inject(BACKEND_URLS) private backendURLs,
        private http: Http)
    {
        this.storage = window.localStorage;
    }

    isAuthenticated() {
        return tokenNotExpired();
    }

    login(username, password) {
        const loginUrl = this.backendURLs.apiBase + this.backendURLs.auth.login;

        const doLogin = (response) => {
            this.token = response.json().token;
            this.storage.setItem(this.settings.authTokenName, this.token);

            return true;
        }

        return this.http.post(loginUrl, {username, password})
                   .map(doLogin);
    }

    logout() {
        this.storage.removeItem(this.settings.authTokenName);
    }

}
