
import { NgModule } from '@angular/core';

import { StoreService } from './store.service';
import { SubmitFormComponent } from './form.component';
import { ElapsedTimePipe } from './pipes';


@NgModule({
    declarations: [
        SubmitFormComponent,
        ElapsedTimePipe,
    ],
    exports: [
        SubmitFormComponent,
        ElapsedTimePipe,
    ],
    providers: [
        StoreService,
    ]
})
export class WebCommonModule { }
