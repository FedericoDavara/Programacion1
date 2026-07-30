import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import jwtDecode from 'jwt-decode';
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
    const params = {
      page: page.toString(),
      per_page: perPage.toString(),
      rol: filtroRol
    };

    return this.httpClient.get(`${this.url}/usuarios`, { params });
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
    return this.httpClient.get(this.url + '/usuario/' + userDNI);
  }

  getUserAlum(userDNI: number){
    return this.httpClient.get(this.url + '/usuario_a/' + userDNI);
  }

  getUserProf(userDNI: number){
    return this.httpClient.get(this.url + '/usuario_p/' + userDNI);
  }


  searchUsers(searchTerm: string, filtroRol: string): Observable<any> {
    const params: any = {
        search_term: searchTerm,
    };

    if (filtroRol) {
        params.rol = filtroRol;
    }

    return this.httpClient.get(`${this.url}/usuarios`, { params });
  }


  registerUser(userData: any) {
    return this.httpClient.post(this.url + '/auth/register', userData);
  }

  updateUser(dni: number, userData: any) {
    return this.httpClient.put(this.url + '/usuario/' + dni, userData);
  }

  deleteUser(dni: number) {
    return this.httpClient.delete(this.url + '/usuario/' + dni);
  }

  createUserAlum(userData: any) {
    return this.httpClient.post(this.url + '/usuarios_a', userData);
  }

  updateUserAlum(dni: number, userData: any) {
    return this.httpClient.put(this.url + '/usuario_a/' + dni, userData);
  }

  createUserProf(userData: any) {
    return this.httpClient.post(this.url + '/usuarios_p', userData);
  }

  updateUserProf(dni: number, userData: any) {
    return this.httpClient.put(this.url + '/usuario_p/' + dni, userData);
  }

  getAllProf(): Observable<any> {
    return this.httpClient.get<any>(this.url + '/usuarios_p');
  }

   deleteUserAlum(dni: number) {
     return this.httpClient.delete(this.url + '/usuario_a/' + dni);
   }

   suspendUser(dni: number, date: string, reason: string): Observable<any> {
      const userData = {
        fecha_suspension: date,
        motivo_suspension: reason
      };
     return this.httpClient.put(this.url + '/usuario/' + dni, userData);
   }

   activateUser(dni: number): Observable<any> {
     const userData = {
       fecha_suspension: null
     };
     return this.httpClient.put(this.url + '/usuario/' + dni, userData);
   }
}