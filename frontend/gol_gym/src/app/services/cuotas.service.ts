import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CuotasService {
  private url = '/api';

  constructor(private httpClient: HttpClient) {}

  getCuotas(estado?: string, alumnoDni?: number) {
    let params = new HttpParams();
    if (estado) params = params.set('estado', estado);
    if (alumnoDni) params = params.set('alumno_dni', alumnoDni.toString());
    return this.httpClient.get(`${this.url}/cuotas`, { params });
  }

  getCuotasAlumno(dni: number) {
    return this.httpClient.get(`${this.url}/cuotas_alumno/${dni}`);
  }

  getCuota(id: number) {
    return this.httpClient.get(`${this.url}/cuota/${id}`);
  }

  createCuota(data: any) {
    return this.httpClient.post(`${this.url}/cuotas`, data);
  }

  registrarPago(id: number) {
    return this.httpClient.put(`${this.url}/cuota/${id}/pagar`, {});
  }

  deleteCuota(id: number) {
    return this.httpClient.delete(`${this.url}/cuota/${id}`);
  }

  procesarVencimientos() {
    return this.httpClient.post(`${this.url}/cuotas/procesar_vencimientos`, {});
  }
}
