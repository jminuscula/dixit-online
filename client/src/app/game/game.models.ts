
export enum GameStatus {
    NEW = 'new',
    ONGOING = 'ongoing',
}


export class Game {
    id: number;
    name: string;
    status: string;
    nPlayers: object;

    constructor(info) {
        this.id = info.id;
        this.name = info.name;
        this.status = info.status;
        this.nPlayers = info.n_players;
    }

    isPlayable() {
        return this.status === GameStatus.NEW;
    }
}


export class GamesCollection {
    public count: Number;
    private games: Game[];
    private playableGames: Game[];

    constructor(games: Game[]) {
        this.count = games.length;
        this.games = games.map((data) => new Game(data));
        this.playableGames = this.games.filter((g) => g.isPlayable())
    }

    select(gameId) {
        for (let game of this.games) {
            if (game.id === gameId) {
                return game;
            }
        }
        return null;
    }

    selectFirstPlayable() {
        if (this.playableGames.length) {
            return this.playableGames[0];
        }
        return null;
    }

}
