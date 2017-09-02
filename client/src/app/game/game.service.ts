
import { Injectable, Inject } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { AuthHttp } from 'angular2-jwt';
import 'rxjs/add/operator/map';

import { BACKEND_URLS } from '../settings/routes';

import { Game } from './game.models';


export enum GameStatus {
    NEW = 'new',
    ONGOING = 'ongoing',
}


@Injectable()
export class GameService {
    private userGamesSubject: BehaviorSubject<Game[]>;

    public userGames: Observable<Game[]>;
    public currentGame: BehaviorSubject<Game>;

    constructor(
        @Inject(BACKEND_URLS) private backendURLs,
        private http: AuthHttp)
    {
        this.userGamesSubject = new BehaviorSubject([]);
        this.currentGame = new BehaviorSubject(null);

        this.userGames = this.userGamesSubject.asObservable().distinctUntilChanged();
        this.userGames.subscribe(this.selectCurrentGame.bind(this));

    }

    selectCurrentGame(games) {
        // TODO: load current game from localStorage
        if (games.length) {
            this.currentGame.next(games[0]);
        }
    }

    loadGames(status: Array<GameStatus> | GameStatus, user: String) {
        const gameListUrl = this.backendURLs.apiBase + this.backendURLs.game;

        const pipeGamesData = (response) => {
            let gamesData = response.json();
            let games = gamesData.map((data) => new Game(data));

            this.userGamesSubject.next(games);
            return games;
        };

        return this.http.get(gameListUrl)
                   .subscribe(pipeGamesData);
    }

}
