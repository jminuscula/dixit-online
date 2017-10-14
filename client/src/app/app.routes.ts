
import { GameManagerComponent } from './game/manager/manager.component';
import { IsAuthenticatedGuard } from './auth/auth.guard';
import { LoginComponent, LogoutComponent } from './auth/login.component';

export const routes = [
    { path: '', component: GameManagerComponent, pathMatch: 'full', canActivate: [IsAuthenticatedGuard],
      children: [
        //   {
        //       path: 'game/:gameId',
        //       component: GameComponent,
        //       pathMatch: 'full',
        //   },
      ]
    },
    { path: 'login', component: LoginComponent },
    { path: 'logout', component: LogoutComponent },
];
