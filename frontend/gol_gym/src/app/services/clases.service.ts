import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class ClasesService {
  url = '/api';
  constructor(
    private httpClient: HttpClient,
  ) { }

  getClases(){
    return this.httpClient.get(this.url + '/clases');
  }

  getClase(claseID: number){
    return this.httpClient.get(this.url + '/clase/' + claseID);
  }

  getClaseProfesor(profDNI: number){
    return this.httpClient.get(this.url + '/clases_por_profesor/' + profDNI);
  }

  createClase(claseData: any) {
    return this.httpClient.post(this.url + '/clases', claseData);
  }

  updateClase(id: number, claseData: any) {
    return this.httpClient.put(this.url + '/clase/' + id, claseData);
  }

  deleteClase(id: number) {
    return this.httpClient.delete(this.url + '/clase/' + id);
  }
}