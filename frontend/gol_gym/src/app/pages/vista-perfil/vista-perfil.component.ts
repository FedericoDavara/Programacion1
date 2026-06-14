import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-vista-perfil',
  templateUrl: './vista-perfil.component.html',
  styleUrls: ['./vista-perfil.component.css']
})
export class VistaPerfilComponent implements OnInit {
  dni: number | null = null;
  rol: string | null = null;

  ngOnInit(): void {
    const dniStr = history.state?.dni || localStorage.getItem('dni');
    this.dni = dniStr ? parseInt(dniStr) : null;
    this.rol = localStorage.getItem('role');
  }
}
