
import { AppRoutes } from './settings/routes';

import { GameComponent } from './game/game.component';
import { IsAuthenticatedGuard } from './auth/auth.guard';
import { LoginComponent, LogoutComponent } from './auth/login.component';


export const routes = [
    { path: AppRoutes.home, component: GameComponent, pathMatch: 'full', canActivate: [IsAuthenticatedGuard],
    //   children: [
    //       { path: AppRoutes.round, component: RoundComponent, pathMatch: 'full' },
    //   ]
    },

    { path: AppRoutes.auth.login, component: LoginComponent },
    { path: AppRoutes.auth.logout, component: LogoutComponent },
];
