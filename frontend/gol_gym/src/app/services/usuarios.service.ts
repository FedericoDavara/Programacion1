import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { jwtDecode } from "/home/victor/Escritorio/Nueva carpeta 1/Programacion1/frontend/gol_gym/node_modules/jwt-decode/build/cjs/index"
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class UsuariosService {
  url = '/api';
  constructor(
    private httpClient: HttpClient,
  ) { }

  getUsers(page: number, perPage: number, filtroRol: string): Observable<any> {
    let auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });

    const params = {
      page: page.toString(),
      per_page: perPage.toString(),
      rol: filtroRol
    };

    return this.httpClient.get(`${this.url}/usuarios`, { headers, params });
  }

  getUserDNIFromToken(): number | null {
    let auth_token = localStorage.getItem('token');
    if (auth_token) {
      const decodedToken: any = jwtDecode(auth_token);
      return decodedToken.dni;
    }
    return null;
  }

  getUser(userDNI: number){
    let auth_token=localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
      return this.httpClient.get(this.url + '/usuario/' + userDNI, {headers: headers});
  }

  getUserAlum(userDNI: number){
    let auth_token=localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
      return this.httpClient.get(this.url + '/usuario_a/' + userDNI, {headers: headers});
  }

  getUserProf(userDNI: number){
    let auth_token=localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
      return this.httpClient.get(this.url + '/usuario_p/' + userDNI, {headers: headers});
  }


  searchUsers(searchTerm: string, filtroRol: string): Observable<any> {
    let auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth_token}`
    });

    const params: any = {
        search_term: searchTerm,
    };

    if (filtroRol) {
        params.rol = filtroRol;
    }

    return this.httpClient.get(`${this.url}/usuarios`, { headers, params });
  }


  createUser(userData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.post(this.url + '/usuarios', userData, { headers: headers });
  }

  updateUser(dni: number, userData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.put(this.url + '/usuario/' + dni, userData, { headers: headers });
  }

  deleteUser(dni: number) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.delete(this.url + '/usuario/' + dni, { headers: headers });
  }

  createUserAlum(userData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.post(this.url + '/usuarios_a', userData,{ headers: headers });
  }

  updateUserAlum(dni: number, userData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.put(this.url + '/usuario_a/' + dni, userData, { headers: headers });
  }

  createUserProf(userData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.post(this.url + '/usuarios_p', userData,{ headers: headers });
  }

  updateUserProf(dni: number, userData: any) {
    const auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return this.httpClient.put(this.url + '/usuario_p/' + dni, userData, { headers: headers });
  }

}
