class MainCards {
    constructor(container, card, counter, api, user, button) {
        this.container = container;
        this.card = card;
        this.user = user;
        this.counter = counter;
        this.target = null;
        this.button = button;
        this._eventUser = this._eventUser.bind(this);

    }
    addEvent() {
        const eventCb = this._eventUser;
        this.container.addEventListener('click', eventCb)
    }
    _eventUser(e) {
        this.target = e.target.closest('button');
    }
}
