import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Http, RequestOptions } from '@angular/http';
import { RouterModule } from '@angular/router';
import { AuthHttp, AuthConfig } from 'angular2-jwt';

import { AuthService } from './auth.service';
import { IsAuthenticatedGuard } from './auth.guard';
import { LoginComponent, LogoutComponent } from './login.component';


export function authHttpServiceFactory(http: Http, options: RequestOptions) {
  return new AuthHttp(new AuthConfig(), http, options);
}


const AuthProvider = {
    provide: AuthHttp,
    useFactory: authHttpServiceFactory,
    deps: [Http, RequestOptions]
};


@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        RouterModule,
    ],
    declarations: [
        LoginComponent,
        LogoutComponent,
    ],
    providers: [
        AuthProvider,
        AuthService,
        IsAuthenticatedGuard,
    ]
})
export class AuthModule {}
