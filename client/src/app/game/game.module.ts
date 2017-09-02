
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

import { GameService } from './game.service';
import { GameComponent } from './game.component';
import { MenuComponent } from './menu/menu.component';


@NgModule({
    imports: [
        RouterModule,
        CommonModule,
    ],
    declarations: [
        GameComponent,
        MenuComponent,
    ],
    providers: [
        GameService,
    ]
})
export class GameModule { }
