import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class PreciosService {
  url = '/api';
  constructor(
    private httpClient: HttpClient,
  ) { }

  getPrecios(){
    return this.httpClient.get(this.url + '/precios');
  }

  getPrecio(precioID: number){
    return this.httpClient.get(this.url + '/precio/' + precioID);
  }

  createPrecio(precioData: any) {
    return this.httpClient.post(this.url + '/precios', precioData);
  }

  updatePrecio(id: number, precioData: any) {
    return this.httpClient.put(this.url + '/precio/' + id, precioData);
  }

  deletePrecio(id: number) {
    return this.httpClient.delete(this.url + '/precio/' + id);
  }
}
