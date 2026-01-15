import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ClasesService } from 'src/app/services/clases.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  arrayPromos = [
    {
      mes:'1 Mes',
      precio:'$9.999',
      info:'1 mes de suscripción estándar.',
    },
    {
      mes:'3 Meses',
      precio:'$24.999',
      info:'Oferta por 3 meses de suscripción.',
    },
    {
      mes:'6 Meses',
      precio:'$44.999',
      info:'Oferta por 6 meses de suscripción.',
    },
    {
      mes:'1 Año',
      precio:'$84.999',
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

  constructor(
    private router: Router,
    private clasesService: ClasesService
  ) {}

  ngOnInit(): void {
    this.cargarClases();
  }

  cargarClases() {
    this.clasesService.getClases().subscribe((data: any) => {
      console.log('JSON data:', data);
      this.arrayClases = data;
    });
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




}
