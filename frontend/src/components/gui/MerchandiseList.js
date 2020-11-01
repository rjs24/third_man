import React, { Component } from 'react';

import MerchandiseService from './service/FinanceService';
const merchandiseService = new MerchandiseService();

class MerchandiseList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tickets: [],
        };
        this.getMerchandises = this.getMerchandises.bind(this);
        this.getMerchandiseByUrl = this.getMerchandiseByUrl.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleUpdate = this.handleUpdate.bind(this);
    }
}
export default MerchandiseList;

getMerchandises() {
    var self = this;
    merchandiseService.getMerchandises().then(function (result) {
        self.setState({ merchandise: result.data, nextPageURL: result.nextlink })
    });
}

getMerchandiseByURL() {
    var self = this;
    merchandiseService.getMerchandiseByURL(this.state.nextPageURL).then((result) => {
        self.setState({merchandise: result.data, nextPageURL: result.nextLink})
    });
}

handleDelete(e,pk) {
    var self = this;
    merchandiseService.deleteMerchandise({pk: pk}).then(() => {
        var newArr = self.state.merchandise.filter(function(obj) {
            return obj.pk !== pk;
        });
        self.setState({merchandise: newArr})
    });

handleUpdate(e,pk) {
    var self = this;
    merchandiseService.updateMerchandise({pk: pk}).then(() => {
        var newArr = self.state.merchandise.filter(function(obj) {
            return obj.pk == pk;
        });
        self.setState({merchandise: newArr})
    });
}

handleCreate(e, pk) {
    var self = this;
    merchandiseService.createMerchandise({pk: pk}).then(() => {
        return obj.pk == pk;
    });
    self.setState({merchandise: newArr })
}
}