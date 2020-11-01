import React, { Component } from 'react';

import BasketService from './service/FinanceService';
const basketService = new BasketService();

class BasketList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tickets: [],
        };
        this.getBasketByUrl = this.getBasketByUrl.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleUpdate = this.handleUpdate.bind(this);
    }
}
export default BasketList;

getBasketByURL() {
    var self = this;
    basketService.getBasketByURL(this.state.nextPageURL).then((result) => {
        self.setState({basket: result.data, nextPageURL: result.nextLink})
    });
}

handleDelete(e,pk) {
    var self = this;
    basketService.deleteBasket({pk: pk}).then(() => {
        var newArr = self.state.tickets.filter(function(obj) {
            return obj.pk !== pk;
        });
        self.setState({baskets: newArr})
    });

handleUpdate(e,pk) {
    var self = this;
    basketService.updateBasket({pk: pk}).then(() => {
        var newArr = self.state.tickets.filter(function(obj) {
            return obj.pk == pk;
        });
        self.setState({tickets: newArr})
    });
}

handleCreate(e, pk) {
    var self = this;
    basketService.createbasket({pk: pk}).then(() => {
        return obj.pk == pk;
    });
    self.setState({tickets: newArr })
}
}