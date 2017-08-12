
import { InjectionToken } from '@angular/core';

export const BACKEND_URLS = new InjectionToken<string>('Backend URLs');

export const BackendRoutesValueProvider = {
    provide: BACKEND_URLS,
    useValue: {
        apiBase: 'http://localhost:8000/api',
        auth: {
            me: '/user/me',
            login: '/user/api-token-auth/'
        }
    }
};
