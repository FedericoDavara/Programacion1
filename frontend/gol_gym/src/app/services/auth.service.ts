import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable, take } from 'rxjs';
import { Router } from '@angular/router'

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = '/api';
  constructor(
    private httpClient: HttpClient,
    private router: Router
  ) { }

  login(dataLogin: any): Observable<any> {
    return this.httpClient.post(this.url + '/auth/login', dataLogin).pipe(take(1));
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('dni');
    localStorage.removeItem('nombre');
    localStorage.removeItem('apellido');
    this.router.navigate(['/', 'home']);
  }
}

