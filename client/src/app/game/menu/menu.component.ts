
import { Component, Input } from '@angular/core';

import { User } from '../../auth/auth.models';


@Component({
    selector: 'menu',
    templateUrl: './menu.component.html',
})
export class MenuComponent {
    @Input() user: User;
}
