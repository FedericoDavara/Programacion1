import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class PreciosService {
  url = '/api';
  constructor(
    private httpClient: HttpClient,
  ) { }

  getPrecios(){  
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
      return this.httpClient.get(this.url + '/precios', {headers: headers});
  }

  getPrecio(precioID: number){
    let auth_token=localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`   
    });
      return this.httpClient.get(this.url + '/precio/' + precioID, {headers: headers});
  }

  createPrecio(precioData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.post(this.url + '/precios', precioData, { headers: headers });
  }

  updatePrecio(id: number, precioData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.put(this.url + '/precio/' + id, precioData, { headers: headers });
  }
  
  deletePrecio(id: number) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.delete(this.url + '/precio/' + id, { headers: headers });
  }
}
