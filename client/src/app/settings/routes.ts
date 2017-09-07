
import { InjectionToken } from '@angular/core';


export const URLS = new InjectionToken<string>('URLs');
export const BACKEND_URLS = new InjectionToken<string>('Backend URLs');

export const AppRoutes = {
    home: '',
    auth: {
        login: 'login',
        logout: 'logout',
    },
    game: 'game/:id',
    round: 'round/:id'
};

export const AppRoutesValueProvider = {
    provide: URLS,
    useValue: AppRoutes,
};

export const BackendRoutesValueProvider = {
    provide: BACKEND_URLS,
    useValue: {
        apiBase: 'http://localhost:8000/api',
        auth: {
            me: '/user/me/',
            login: '/user/api-token-auth/'
        },
        game: '/game/',
    }
};
