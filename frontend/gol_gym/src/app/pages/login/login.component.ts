import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service'
import { Router } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm!: FormGroup;

  constructor(
    private authService: AuthService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['cr7@gmail.com', Validators.required],
      password: ['madrid15', Validators.required]
    })
  }

  login(dataLogin: any={}){
    //dataLogin = {email:'cr7@gmail.com', password:'madrid15'}
    console.log('comprobando credenciales');
    this.authService.login(dataLogin).subscribe({
      next: (rta: any) => {
        alert('login exitoso');
        console.log('respuesta login:', rta.access_token);
        localStorage.setItem('token', rta.access_token);
        this.router.navigateByUrl('home');
      },error: (error) => {
        alert('Credenciales incorrectas');
        localStorage.removeItem('token');

      }, complete: () => {
        console.log('finalizo')
      }
    })
  }
  
  submit(){
    if(this.loginForm.valid){
      console.log('Form login: ',this.loginForm.value);
      this.login (this.loginForm.value);
    } else {
      alert('Formulario invalido');
    }
  }
}