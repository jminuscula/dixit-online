
import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs';
import { distinctUntilChanged } from 'rxjs/operators';

import { SETTINGS } from '../settings/base';
import { BACKEND_URLS } from '../settings/routes';

import { User } from './auth.models';


@Injectable()
export class UserService {
    private currentUserSubject: Subject<User>;
    public currentUser: Observable<User>;

    constructor(
        @Inject(SETTINGS) private settings,
        @Inject(BACKEND_URLS) private backendURLs,
        private http: HttpClient)
    {
        this.currentUserSubject = new Subject();
        this.currentUser = this.currentUserSubject.asObservable().pipe(distinctUntilChanged());
    }

    updateCurrentUser() {
        const loginUrl = `${this.backendURLs.apiBase}/${this.backendURLs.auth.me}`;

        const pipeUserInfo = (response) => {
            let info = response.json();
            let user = new User(info);
            this.currentUserSubject.next(user);
        }

        return this.http.get(loginUrl)
                   .subscribe(pipeUserInfo);
    }

}
