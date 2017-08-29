
export class User {
    username: string;
    email: string;
    profile: object;

    constructor(info) {
        this.username = info.username;
        this.email = info.email
        this.profile = info.profile;
    }
}
