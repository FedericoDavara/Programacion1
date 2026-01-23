import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-navclose',
  templateUrl: './navclose.component.html',
  styleUrls: ['./navclose.component.css']
})
export class NavcloseComponent implements OnInit {
  nombreUsuario: string | null = '';
  rolUsuario: string | null = '';

  constructor(
    private authService: AuthService
  ) {}

  ngOnInit() {
    const nombre = localStorage.getItem('nombre');
    const apellido = localStorage.getItem('apellido');
    this.rolUsuario = localStorage.getItem('role');

    if (nombre && apellido) {
      this.nombreUsuario = `${nombre} ${apellido}`;
    }
  }

  cerrarSesion() {
    this.authService.logout();
  }
}
