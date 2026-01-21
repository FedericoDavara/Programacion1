import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ContactoData {
  nombre: string;
  email: string;
  mensaje: string;
}

export interface ContactoResponse {
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ContactoService {
  private url = '/api';

  constructor(private httpClient: HttpClient) { }

  enviarMensaje(data: ContactoData): Observable<ContactoResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    return this.httpClient.post<ContactoResponse>(this.url + '/contacto', data, { headers });
  }
}
