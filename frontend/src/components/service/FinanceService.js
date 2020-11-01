import axios from 'axios';
const API_URL = 'http://localhost:8000';

export default class TicketService{

    constructor(){}

    getTickets() {
        const url = `${API_URL}/api/ticket/`;
        return axios.get(url).then(response => response.data);
    }
    getTicketsByURL(link){
        const url = `${API_URL}/ticket/${link}`;
        return axios.get(url).then(response => response.data);
    }
    deleteTicket(ticket){
        const url = `${API_URL}/api/ticket/${ticket.pk}`;
        return axios.delete(url);
    }
    createTicket(ticket){
        const url = `${API_URL}/api/ticket/`;
        return axios.post(url,ticket);
    }
    updateTicket(ticket){
        const url = `${API_URL}/api/ticket/${ticket.pk}`;
        return axios.put(url,ticket);
    }
}

export default class DonationService{

    constructor(){}

    getDonations() {
    const url = `${API_URL}/api/ticket/`;
    return axios.get(url).then(response => response.data);
    }
    getDonationsByURL(link){
        const url = `${API_URL}/api/donation/${link}`;
        return axios.get(url).then(response => response.data);
    }
    deleteDonation(donation){
        const url = `${API_URL}/api/donation/${donation.pk}`;
        return axios.delete(url);
    }
    createDonation(donation){
        const url = `${API_URL}/api/donation/`;
        return axios.post(url,donation);
    }
    updateDonation(donation){
        const url = `${API_URL}/api/donation/${donation.pk}`;
        return axios.put(url,donation);
    }
}

export class MerchandiseService{

    constructor(){}

    getMerchandise() {
    const url = `${API_URL}/api/merchandise/`;
    return axios.get(url).then(response => response.data);
    }
    getMerchandiseByURL(link){
        const url = `${API_URL}/api/merchandise/${link}`;
        return axios.get(url).then(response => response.data);
    }
    deleteMerchandise(merchandise){
        const url = `${API_URL}/api/merchandise/${merchandise.pk}`;
        return axios.delete(url);
    }
    createMerchandise(merchandise){
        const url = `${API_URL}/api/merchandise/`;
        return axios.post(url,merchandise);
    }
    updateMerchandise(merchandise){
        const url = `${API_URL}/api/merchandise/${merchandise.pk}`;
        return axios.put(url,merchandise);
    }
}

export class GiftaidService{

    constructor(){}

     getGiftaid() {
    const url = `${API_URL}/api/giftaid/`;
    return axios.get(url).then(response => response.data);
    }
    getGiftaidByURL(link){
        const url = `${API_URL}/api/giftaid/${link}`;
        return axios.get(url).then(response => response.data);
    }
    deleteGiftaid(giftaid){
        const url = `${API_URL}/api/giftaid/${giftaid.pk}`;
        return axios.delete(url);
    }
    createGiftaid(giftaid){
        const url = `${API_URL}/api/giftaid/`;
        return axios.post(url,giftaid);
    }
    updateGiftaid(giftaid){
        const url = `${API_URL}/api/giftaid/${giftaid.pk}`;
        return axios.put(url,giftaid);
    }
}

export class BasketService{

    constructor(){}

    getBasket() {
    const url = `${API_URL}/api/basket/`;
    return axios.get(url).then(response => response.data);
    }
    getBasketByURL(link){
        const url = `${API_URL}/api/basket/${link}`;
        return axios.get(url).then(response => response.data);
    }
    deleteBasket(giftaid){
        const url = `${API_URL}/api/basket/${basket.pk}`;
        return axios.delete(url);
    }
    createBasket(basket){
        const url = `${API_URL}/api/basket/`;
        return axios.post(url,basket);
    }
    updateBasket(basket){
        const url = `${API_URL}/api/basket/${basket.pk}`;
        return axios.put(url,basket);
    }
}