
import { Injectable, Inject } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { AuthHttp } from 'angular2-jwt';
import 'rxjs/add/operator/map';

import { BACKEND_URLS } from '../settings/routes';

import { StoreService } from '../webcommon/store.service';
import { GamesCollection, Game, GameStatus } from './game.models';


@Injectable()
export class GameService {
    private userGamesSubject: BehaviorSubject<GamesCollection>;

    public userGames: Observable<GamesCollection>;
    public currentGame: BehaviorSubject<Game>;

    constructor(
        @Inject(BACKEND_URLS) private backendURLs,
        private store: StoreService,
        private http: AuthHttp)
    {
        this.userGamesSubject = new BehaviorSubject(new GamesCollection([]));
        this.currentGame = new BehaviorSubject(null);

        this.userGames = this.userGamesSubject.asObservable().distinctUntilChanged();
        this.userGames.subscribe(this.selectCurrentGame.bind(this));
    }

    selectCurrentGame(games) {
        let latestGameId = this.store.get(this.store.keys.lastGameId);
        let current = games.select(latestGameId);
        if (!current || !current.isPlayable()) {
            current = games.selectFirstPlayable();
            if (current) {
                this.store.set(this.store.keys.lastGameId, current.id);
            }
        }

        this.currentGame.next(current);
    }

    loadGames(status: Array<GameStatus> | GameStatus, user: String) {
        const gameListUrl = this.backendURLs.apiBase + this.backendURLs.game;

        const pipeGamesData = (response) => {
            let gamesData = response.json();
            let collection = new GamesCollection(gamesData);
            this.userGamesSubject.next(collection);
            return collection;
        };

        return this.http.get(gameListUrl)
                   .subscribe(pipeGamesData);
    }

}
