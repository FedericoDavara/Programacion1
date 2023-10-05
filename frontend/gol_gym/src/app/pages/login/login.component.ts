import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  constructor(
    private authService: AuthService
  ) {}
  login(dataLogin: any={}){
    console.log('comprobando credenciales');
    this.authService.login().subscribe({
      next: (rta: any) => {
        alert('login exitoso');
        console.log('respuesta login:', rta);

      },error: (error) => {

      }, complete: () => {
        console.log('finalizo')
      }
    })
  }  
}
