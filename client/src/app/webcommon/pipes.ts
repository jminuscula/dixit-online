
import { Pipe, PipeTransform } from '@angular/core';


@Pipe({
    name: 'elapsedTime'
})
export class ElapsedTimePipe implements PipeTransform {
    partNames = [
        ['year', 'y'], ['month', 'mo'], ['day', 'd'],
        ['hour', 'h'], ['minute', 'm'], ['second', 's'],
    ];

    datePartsMilliseconds = {
        year: 1000 * 60 * 60 * 24 * 365,
        month: 1000 * 60 * 60 * 24 * 30,
        day: 1000 * 60 * 60 * 24,
        hour: 1000 * 60 * 60,
        minute: 1000 * 60,
        seconds: 1000,
    };

    getDatePartsFromSeconds(seconds) {
        let result: any = {};
        for (let part in this.datePartsMilliseconds) {
            let ms = this.datePartsMilliseconds[part];
            let partMs = Math.floor(seconds / ms);
            if (partMs > 0) {
                result[part] = partMs;
                seconds = seconds - (partMs * ms);
            }
        }
        return result;
    }

    transform(value: Date): String {
        let now = new Date();
        let deltaSeconds = now.getTime() - value.getTime();
        let parts = this.getDatePartsFromSeconds(deltaSeconds);
        let elapsed = [];

        for (let [partName, partSymbol] of this.partNames) {
            if (parts[partName]) {
                elapsed.push(parts[partName] + partSymbol);
                if (elapsed.length == 2) {
                    break;
                }
            }
        }

        return elapsed.join(', ');
    }
}
