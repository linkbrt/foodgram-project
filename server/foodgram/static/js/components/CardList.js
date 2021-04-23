class CardList extends MainCards {
    _eventUser(e) {
        super._eventUser(e);
        if (this.target && this.target.name === 'purchases') {
            this._eventPurchases(this.target)
        }
        if (this.target && this.target.name === 'favorites') {
            this._eventFavorites(this.target);
        }
    }
    _eventFavorites(target) {
        const cardId = target.closest(this.card).getAttribute('data-id');
        if(target.hasAttribute('data-out')) {
            this.button.favorites.addFavorites(target,cardId)
        } else {
            this.button.favorites.removeFavorites(target,cardId)
        }
    }
    _eventPurchases(target)  {
        const cardId = target.closest(this.card).getAttribute('data-id');
        if(target.hasAttribute('data-out')) {
            this.button.purchases.addPurchases(target,cardId, this.counter.plusCounter)
        } else {
            this.button.purchases.removePurchases(target,cardId,this.counter.minusCounter);

        }
    }
}
