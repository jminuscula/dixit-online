
import { InjectionToken } from '@angular/core';

export const SETTINGS = new InjectionToken<string>('Settings');

export const SettingsValueProvider = {
    provide: SETTINGS,
    useValue: {
        authTokenName: 'token',
    }
};
