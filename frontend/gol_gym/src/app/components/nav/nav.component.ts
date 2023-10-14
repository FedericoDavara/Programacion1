import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent {
  verRutas = true;
  constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  get isToken() {
    return localStorage.getItem('token');
  }

  cerrarSesion() {
    this.authService.logout();
  }

}