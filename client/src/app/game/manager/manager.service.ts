
import { Injectable, Inject } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import { AuthHttp } from 'angular2-jwt';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';

import { BACKEND_URLS } from 'settings/routes';

import { StoreService } from 'webcommon/store.service';
import { Game, GameStatus } from 'game/game.models';


@Injectable()
export class GameManagerService {
    private gamesSubject: Subject<Game[]>;

    public currentGame: Subject<Game>;
    public playableGames: Observable<Game[]>;
    public games: Observable<Game[]>;

    constructor(
        @Inject(BACKEND_URLS) private backendURLs,
        private store: StoreService,
        private http: AuthHttp)
    {
        this.gamesSubject = new Subject();
        this.games = this.gamesSubject.asObservable();
        this.playableGames = this.games.filter(this.getPlayableGames);
    }

    loadGames(status: Array<GameStatus> | GameStatus, user: String) {
        const gameListUrl = this.backendURLs.apiBase + this.backendURLs.game;

        const pipeGamesData = (response) => {
            let gamesData = response.json();
            let games = gamesData.map((data) => new Game(data));
            this.gamesSubject.next(games);
        };

        return this.http.get(gameListUrl)
                   .subscribe(pipeGamesData);
    }

    getPlayableGames(games) {
        return games.filter((game) => game.isPlayable());
    }
}
