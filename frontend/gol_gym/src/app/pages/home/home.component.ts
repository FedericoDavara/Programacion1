import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ClasesService } from 'src/app/services/clases.service';
import { ContactoService } from 'src/app/services/contacto.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  arrayPromos = [
    {
      mes:'1 Mes',
      precio:'$12.000',
      info:'1 mes de suscripción estándar.',
    },
    {
      mes:'3 Meses',
      precio:'$14.900',
      info:'Oferta por 3 meses de suscripción.',
    },
    {
      mes:'6 Meses',
      precio:'$19.999',
      info:'Oferta por 6 meses de suscripción.',
    },
    {
      mes:'1 Año',
      precio:'$114.000',
      info:'Oferta por 1 año de suscripción.',
    }
  ]
  arrayProfes = [
    {
      foto:'assets/profe2.jpg',
      nombre:'Michael Jordan',
      info:'Leyenda del baloncesto.',
    },
    {
      foto:'assets/profe3.jpg',
      nombre:'Mike Tyson',
      info:'Campeón de boxeo.',
    },
    {
      foto:'assets/profe4.jpg',
      nombre:'Paula Pareto',
      info:'Judoka olímpica.',
    },
  ]

  arrayClases: any;

  // Formulario de contacto
  contactoForm: FormGroup;
  enviando: boolean = false;
  mensajeExito: string = '';
  mensajeError: string = '';

  constructor(
    private router: Router,
    private clasesService: ClasesService,
    private contactoService: ContactoService,
    private fb: FormBuilder
  ) {
    this.contactoForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      mensaje: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  ngOnInit(): void {
    this.cargarClases();
  }

  cargarClases() {
    this.clasesService.getClases().subscribe((data: any) => {
      console.log('JSON data:', data);
      this.arrayClases = data;
    });
  }

  scrollToClases() {
    const elementoDestino = document.getElementById('Clasesid');
    if (elementoDestino) {
      elementoDestino.scrollIntoView({ behavior: 'smooth' });
    }
  }

  getClasesPorDia(dia: string): any {
    if (this.arrayClases) {
      return this.arrayClases
        .filter((clase: any) => clase.dia === dia)
        .sort((a: any, b: any) => {
          const horaA = parseInt(a.horario.split(":")[0]);
          const minutoA = parseInt(a.horario.split(":")[1]);
          const horaB = parseInt(b.horario.split(":")[0]);
          const minutoB = parseInt(b.horario.split(":")[1]);

          if (horaA !== horaB) {
            return horaA - horaB;
          } else {
            return minutoA - minutoB;
          }
        });
    } else {
      return []
    }
  }

  enviarContacto() {
    // Limpiar mensajes previos
    this.mensajeExito = '';
    this.mensajeError = '';

    // Validar formulario
    if (this.contactoForm.invalid) {
      this.contactoForm.markAllAsTouched();
      return;
    }

    this.enviando = true;

    this.contactoService.enviarMensaje(this.contactoForm.value).subscribe({
      next: (response) => {
        this.mensajeExito = 'Mensaje enviado correctamente. Nos pondremos en contacto pronto.';
        this.contactoForm.reset();
        this.enviando = false;
      },
      error: (error) => {
        this.mensajeError = error.error?.message || 'Error al enviar el mensaje. Intente nuevamente.';
        this.enviando = false;
      }
    });
  }
}
