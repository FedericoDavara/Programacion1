import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PlanificacionService {
  url = '/api';

  constructor(private httpClient: HttpClient) {}

  getPlanif(userDNI: number) {
    return this.httpClient.get(this.url + '/planificacion_a/' + userDNI);
  }

  createPlanif(planificacionData: any) {
    return this.httpClient.post(this.url + '/planificaciones', planificacionData);
  }

  updatePlanif(id: number, planificacionData: any) {
    return this.httpClient.put(this.url + '/planificacion/' + id, planificacionData);
  }

  deletePlanif(id: number) {
    return this.httpClient.delete(this.url + '/planificacion/' + id);
  }
}
