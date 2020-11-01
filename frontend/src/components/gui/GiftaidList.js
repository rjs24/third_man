import React, { Component } from 'react';

import GiftaidService from './service/FinanceService';
const giftaidService = new GiftaidService();

class GiftaidList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tickets: [],
        };
        this.getGiftaid = this.getGiftaid.bind(this);
        this.getGiftaidByUrl = this.getGiftaidByUrl.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleUpdate = this.handleUpdate.bind(this);
    }
}
export default GiftaidList;

getGiftaid() {
    var self = this;
    giftaidService.getGiftaid().then(function (result) {
        self.setState({ giftaid: result.data, nextPageURL: result.nextlink })
    });
}

getGiftaidByURL() {
    var self = this;
    giftaidService.getDonationByURL(this.state.nextPageURL).then((result) => {
        self.setState({giftaid: result.data, nextPageURL: result.nextLink})
    });
}

handleDelete(e,pk) {
    var self = this;
    giftaidService.deleteGiftaid({pk: pk}).then(() => {
        var newArr = self.state.giftaid.filter(function(obj) {
            return obj.pk !== pk;
        });
        self.setState({giftaid: newArr})
    });

handleUpdate(e,pk) {
    var self = this;
    giftaidService.updateGiftaid({pk: pk}).then(() => {
        var newArr = self.state.giftaid.filter(function(obj) {
            return obj.pk == pk;
        });
        self.setState({giftaid: newArr})
    });
}

handleCreate(e, pk) {
    var self = this;
    giftaidService.createGiftaid({pk: pk}).then(() => {
        return obj.pk == pk;
    });
    self.setState({giftaid: newArr })
}
}