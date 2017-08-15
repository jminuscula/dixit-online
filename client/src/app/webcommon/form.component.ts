
import { Component } from '@angular/core';


@Component({
    selector: 'submit-form',
    inputs: ['value'],
    template: `
        <div class="form-field form-submit">
            <input type="submit" style="display: none;" #submit />
            <span class="button" (click)="submit.click()">{{ value }}</span>
        </div>
    `
})
export class SubmitFormComponent {
}
