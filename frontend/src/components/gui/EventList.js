import React, { Component } from 'react';

import EventService from './service/EventService';
const eventsService = new EventService();

class EventList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            events: [],
            nextPageURL: ''
        };
        this.nextPage = this.nextPage.bind(this);
    }
}
export default EventList;

getEvents() {
    var self = this;
    eventsService.getEvents().then(function (result) {
        self.setState({ events: result.data, nextPageURL: result.nextlink })
    });
}

getEventByURL() {
    var self = this;
    eventsService.getEventByURL(this.state.nextPageURL).then((result) => {
        self.setState({events: result.data, nextPageURL: result.nextLink})
    });
}


