import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { jwtDecode } from "/home/victor/Escritorio/Nueva carpeta 1 (copia)/Programacion1/frontend/gol_gym/node_modules/jwt-decode/build/cjs/index"


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm!: FormGroup;
  isToken: boolean = false; // Inicialmente, el usuario no ha iniciado sesión

  constructor(
    private authService: AuthService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['cr7@gmail.com', Validators.required],
      password: ['madrid15', Validators.required]
    });
  }

  login(dataLogin:any = {} ){
    //dataLogin = {email: 'johnnylawrence@nomail.com', password: 'clave1234'}
    console.log('comprobando credenciales');
    this.authService.login(dataLogin).subscribe({
      next: (rta:any) => {
        console.log('Respuesta login: ',rta.access_token);
        localStorage.setItem('token', rta.access_token)

        const decodedToken: any = jwtDecode(rta.access_token);
        localStorage.setItem('role', decodedToken.rol)
        localStorage.setItem('dni', decodedToken.dni)

        if (localStorage.getItem('role') === 'admin' || localStorage.getItem('role') === 'profesor') {
          this.router.navigateByUrl('usuarios');
        } else if (localStorage.getItem('role') === 'user') {
          this.router.navigateByUrl('/vPerfil');
        } else {
          console.error('No posee rol de usuario');
        }

      }, error:(error) => {
          alert('Credenciales incorrectas');
          localStorage.removeItem('dni');
          localStorage.removeItem('role');
          localStorage.removeItem('token');
          
      }, complete: () => {
        console.log('Finalizo')
      }
    })
  }

  submit() {
    if(this.loginForm.valid) {
      console.log('Form login: ',this.loginForm.value);
      this.login(this.loginForm.value)
    } else {
      alert('Formulario inválido');
    }
  }
}