import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpRequest } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { JwtModule } from '@auth0/angular-jwt';

import { WebCommonModule } from '../webcommon/webcommon.module';

import { AuthService } from './auth.service';
import { UserService } from './user.service';
import { IsAuthenticatedGuard } from './auth.guard';
import { LoginComponent, LogoutComponent } from './login.component';


@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        RouterModule,
        WebCommonModule,

        HttpClientModule,
        JwtModule.forRoot({
            config: {
                tokenGetter: () => localStorage.getItem("access_token"),
            }
        }),
    ],
    declarations: [
        LoginComponent,
        LogoutComponent,
    ],
    providers: [
        AuthService,
        UserService,
        IsAuthenticatedGuard,
    ]
})
export class AuthModule {}
