class MyFollow extends MainCards{
    _eventUser (e) {
        super._eventUser(e);
        if (this.target && this.target.name === 'subscribe') {
            this._eventSubscribe(this.target)
        }
    }

    _eventSubscribe  (target)  {
        const authorId = target.closest(this.card).getAttribute('data-author');
        if(target.hasAttribute('data-out')) {
            this.button.subscribe.addSubscribe(target, authorId)
        } else {
            this.button.subscribe.removeSubscribe(target, authorId)
        }
    }

}
