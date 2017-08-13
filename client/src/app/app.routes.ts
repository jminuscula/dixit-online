
import { GameComponent } from './game/game.component';
import { IsAuthenticatedGuard } from './auth/auth.guard';
import { LoginComponent, LogoutComponent } from './auth/login.component';

export const routes = [
    { path: '', component: GameComponent, pathMatch: 'full', canActivate: [IsAuthenticatedGuard] },
    { path: 'login', component: LoginComponent },
    { path: 'logout', component: LogoutComponent },
];
