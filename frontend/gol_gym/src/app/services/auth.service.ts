import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable,take } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // url = 'http://127.0.0.1:5000';
  url = '/api';
  constructor(
    private httpClient: HttpClient
  ) { }
  login(): Observable<any> {
    let dataLogin = {email:'cr7@gmail.com', password:'madrid15'}
    return this.httpClient.post(this.url + '/auth/login',dataLogin).pipe(take(1))
  }
}