
import { NgModule } from '@angular/core';

import { StoreService } from './store.service';
import { SubmitFormComponent } from './form.component';


@NgModule({
    declarations: [
        SubmitFormComponent,
    ],
    exports: [
        SubmitFormComponent,
    ],
    providers: [
        StoreService,
    ]
})
export class WebCommonModule { }
