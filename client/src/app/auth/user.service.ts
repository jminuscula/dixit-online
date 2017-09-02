
import { Injectable, Inject } from '@angular/core';
import { AuthHttp } from 'angular2-jwt';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/distinctUntilChanged';

import { SETTINGS } from '../settings/base';
import { BACKEND_URLS } from '../settings/routes';

import { User } from './auth.models';


@Injectable()
export class UserService {
    private userSubject: Subject<User>;
    public userInfo: Observable<User>;

    constructor(
        @Inject(SETTINGS) private settings,
        @Inject(BACKEND_URLS) private backendURLs,
        private http: AuthHttp)
    {
        this.userSubject = new Subject();
        this.userInfo = this.userSubject.asObservable().distinctUntilChanged();
    }

    updateUserInfo() {
        const loginUrl = this.backendURLs.apiBase + this.backendURLs.auth.me;

        const pipeUserInfo = (response) => {
            let info = response.json();
            let user = new User(info);
            this.userSubject.next(user);
        }

        return this.http.get(loginUrl)
                   .subscribe(pipeUserInfo);
    }

}
