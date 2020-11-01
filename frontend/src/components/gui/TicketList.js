import React, { Component } from 'react';

import TicketService from './service/FinanceService';
const ticketsService = new TicketService();

class TicketList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tickets: [],
        };
        this.getTickets = this.getTickets.bind(this);
        this.getTicketByUrl = this.getTicketByUrl.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleUpdate = this.handleUpdate.bind(this);
    }
}
export default TicketList;

getTickets() {
    var self = this;
    ticketsService.getTickets().then(function (result) {
        self.setState({ tickets: result.data, nextPageURL: result.nextlink })
    });
}

getTicketByURL() {
    var self = this;
    ticketsService.getTicketByURL(this.state.nextPageURL).then((result) => {
        self.setState({tickets: result.data, nextPageURL: result.nextLink})
    });
}

handleDelete(e,pk) {
    var self = this;
    ticketsService.deleteTicket({pk: pk}).then(() => {
        var newArr = self.state.tickets.filter(function(obj) {
            return obj.pk !== pk;
        });
        self.setState({tickets: newArr})
    });

handleUpdate(e,pk) {
    var self = this;
    ticketsService.updateTicket({pk: pk}).then(() => {
        var newArr = self.state.tickets.filter(function(obj) {
            return obj.pk == pk;
        });
        self.setState({tickets: newArr})
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

