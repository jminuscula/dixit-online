
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { GameComponent } from './game.component';
import { MenuComponent } from './menu/menu.component';


@NgModule({
    imports: [
        RouterModule,
    ],
    declarations: [
        GameComponent,
        MenuComponent,
    ],
})
export class GameModule { }
