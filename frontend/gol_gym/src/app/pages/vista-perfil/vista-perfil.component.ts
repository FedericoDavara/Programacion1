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
    // Orden de prioridad:
    // 1. history.state (navegación normal desde otro componente)
    // 2. sessionStorage (recarga de página — persiste en la misma pestaña)
    // 3. localStorage (fallback: el propio usuario logueado)
    const fromNav = history.state?.dni;
    if (fromNav) {
      sessionStorage.setItem('viewed_dni', String(fromNav));
      this.dni = parseInt(fromNav);
    } else {
      const fromSession = sessionStorage.getItem('viewed_dni');
      const fromLocal   = localStorage.getItem('dni');
      const dniStr = fromSession || fromLocal;
      this.dni = dniStr ? parseInt(dniStr) : null;
    }

    this.rol = localStorage.getItem('role');
  }
}
