
import { Injectable } from '@angular/core';


@Injectable()
export class StoreService {
    public keys = {
        lastGameId: 'lastGameId'
    };

    constructor() {}

    get(key, fallback?) {
        let value = window.localStorage.getItem(key);
        return (value !== undefined) ? JSON.parse(value) : fallback;
    }

    set(key, value) {
        window.localStorage.setItem(key, JSON.stringify(value));
    }

}
