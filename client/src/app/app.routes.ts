
import { GameManagerComponent } from './game/manager/manager.component';
import { IsAuthenticatedGuard } from './auth/auth.guard';
import { LoginComponent, LogoutComponent } from './auth/login.component';

import { DebugScreen } from 'game/debug.component';


export const routes = [
    { path: '', component: GameManagerComponent, canActivate: [IsAuthenticatedGuard],
      children: [
          {
              path: 'game/:gameId',
              component: DebugScreen,
              pathMatch: 'full',
          },
      ]
    },
    { path: 'login', component: LoginComponent },
    { path: 'logout', component: LogoutComponent },
];
