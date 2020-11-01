import React, { Component } from 'react';

import DonationService from './service/FinanceService';
const donationService = new DonationService();

class DonationList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tickets: [],
        };
        this.getDonation = this.getDonation.bind(this);
        this.getDonationByUrl = this.getDonationByUrl.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleUpdate = this.handleUpdate.bind(this);
    }
}
export default DonationList;

getDonations() {
    var self = this;
    donationService.getDonations().then(function (result) {
        self.setState({ donation: result.data, nextPageURL: result.nextlink })
    });
}

getDonationByURL() {
    var self = this;
    donationsService.getDonationByURL(this.state.nextPageURL).then((result) => {
        self.setState({donations: result.data, nextPageURL: result.nextLink})
    });
}

handleDelete(e,pk) {
    var self = this;
    donationService.deleteDonation({pk: pk}).then(() => {
        var newArr = self.state.donations.filter(function(obj) {
            return obj.pk !== pk;
        });
        self.setState({donations: newArr})
    });

handleUpdate(e,pk) {
    var self = this;
    donationsService.updateDonation({pk: pk}).then(() => {
        var newArr = self.state.donations.filter(function(obj) {
            return obj.pk == pk;
        });
        self.setState({donations: newArr})
    });
}

handleCreate(e, pk) {
    var self = this;
    ticketsService.createTicket({pk: pk}).then(() => {
        return obj.pk == pk;
    });
    self.setState({tickets: newArr })
}
}