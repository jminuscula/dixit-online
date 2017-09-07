import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';

import { AuthModule } from './auth/auth.module';
import { GameModule } from './game/game.module';

import { AppComponent } from './app.component';
import { routes } from './app.routes';
import { AppRoutesValueProvider, BackendRoutesValueProvider } from './settings/routes';
import { SettingsValueProvider } from './settings/base';


@NgModule({
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        RouterModule.forRoot(routes),

        AuthModule,
        GameModule
    ],
    providers: [
        AppRoutesValueProvider,
        BackendRoutesValueProvider,
        SettingsValueProvider,
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
