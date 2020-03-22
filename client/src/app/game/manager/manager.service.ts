
import { Injectable, Inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs';
import { BehaviorSubject } from 'rxjs';

import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { filter } from 'rxjs/operators';

import { BACKEND_URLS } from 'settings/routes';

import { StoreService } from 'webcommon/store.service';
import { Game, GameStatus } from 'game/game.models';


@Injectable()
export class GameManagerService {
    private gamesSubject: BehaviorSubject<Game[]>;

    public games: Observable<Game[]>;
    public playableGames: Observable<Game[]>;

    constructor(
        @Inject(BACKEND_URLS) private backendURLs,
        private store: StoreService,
        private http: HttpClient)
    {
        this.gamesSubject = new BehaviorSubject([]);
        this.games = this.gamesSubject.asObservable();
        this.playableGames = this.games.pipe(filter(this.playableGamesFilter));
    }

    loadGames(status: Array<GameStatus> | GameStatus, user: String) {
        const gameListUrl = `${this.backendURLs.apiBase}/${this.backendURLs.game}`;

        const pipeGamesData = (response) => {
            let gamesData = response.json();
            let games = gamesData.map((data) => new Game(data));
            console.log('loading games', games);
            this.gamesSubject.next(games);
        };

        return this.http.get(gameListUrl)
                   .subscribe(pipeGamesData);
    }

    playableGamesFilter(games) {
        return games.filter((game) => game.isPlayable());
    }

    getGame(gameId) {
        const gameUrl = `${this.backendURLs.apiBase}/${this.backendURLs.game}/${gameId}`;
        return Observable.create(gameObserver => {
            const getGameDetails = (response) => {
                let data = response.json();
                gameObserver.next(new Game(data));
            };
            this.http.get(gameUrl).subscribe(getGameDetails);
        });
    }
}
