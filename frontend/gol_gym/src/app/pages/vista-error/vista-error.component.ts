import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-vista-error',
  templateUrl: './vista-error.component.html',
  styleUrls: ['./vista-error.component.css']
})
export class VistaErrorComponent implements OnInit {
  isSuspended = false;
  fecha: string = '';
  motivo: string = '';

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.isSuspended = params['suspended'] === 'true';
      this.fecha = params['fecha'] || '';
      this.motivo = params['motivo'] || '';
    });
  }

  salir(): void {
    localStorage.clear();
    this.router.navigate(['/']);
  }
}
