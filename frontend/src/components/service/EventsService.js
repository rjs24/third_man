import axios from 'axios';
const API_URL = 'http://localhost:8000/';

export default class EventsService{

    constructor(){}


    getEvents() {
        const url = `${API_URL}/api/events/`;
        return axios.get(url).then(response => response.data);
    }
    getEventByURL(link){
        const url = `${API_URL}/api/events/${link}`;
        return axios.get(url).then(response => response.data);
    }

}
