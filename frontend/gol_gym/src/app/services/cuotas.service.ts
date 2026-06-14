import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CuotasService {
  private url = '/api';

  constructor(private httpClient: HttpClient) {}

  private get headers(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    });
  }

  getCuotas(estado?: string, alumnoDni?: number) {
    let params = new HttpParams();
    if (estado) params = params.set('estado', estado);
    if (alumnoDni) params = params.set('alumno_dni', alumnoDni.toString());
    return this.httpClient.get(`${this.url}/cuotas`, { headers: this.headers, params });
  }

  getCuotasAlumno(dni: number) {
    return this.httpClient.get(`${this.url}/cuotas_alumno/${dni}`, { headers: this.headers });
  }

  getCuota(id: number) {
    return this.httpClient.get(`${this.url}/cuota/${id}`, { headers: this.headers });
  }

  createCuota(data: any) {
    return this.httpClient.post(`${this.url}/cuotas`, data, { headers: this.headers });
  }

  registrarPago(id: number) {
    return this.httpClient.put(`${this.url}/cuota/${id}/pagar`, {}, { headers: this.headers });
  }

  deleteCuota(id: number) {
    return this.httpClient.delete(`${this.url}/cuota/${id}`, { headers: this.headers });
  }

  procesarVencimientos() {
    return this.httpClient.post(`${this.url}/cuotas/procesar_vencimientos`, {}, { headers: this.headers });
  }
}
