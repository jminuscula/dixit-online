
export class Game {
    name: string;
    status: string;
    nPlayers: object;

    constructor(info) {
        this.name = info.name;
        this.status = info.status;
        this.nPlayers = info.n_players;
    }
}
