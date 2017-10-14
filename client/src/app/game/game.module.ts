
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GameManagerModule } from 'game/manager/manager.module';
import { WebCommonModule } from 'webcommon/webcommon.module';

import { DebugScreen } from 'game/debug.component';


@NgModule({
    imports: [
        CommonModule,
        GameManagerModule,
        WebCommonModule,
    ],
    declarations: [
        DebugScreen,
    ],
    providers: [
    ]
})
export class GameModule { }
