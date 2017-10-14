
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

import { GameManagerService } from 'game/manager/manager.service';
import { GameManagerComponent } from 'game/manager/manager.component';
import { MenuComponent } from 'game/manager/menu/menu.component';
import { WebCommonModule } from 'webcommon/webcommon.module';


@NgModule({
    imports: [
        RouterModule,
        CommonModule,
        WebCommonModule,
    ],
    declarations: [
        GameManagerComponent,
        MenuComponent,
    ],
    providers: [
        GameManagerService,
    ]
})
export class GameManagerModule { }
