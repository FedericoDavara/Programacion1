import { Component, Input, OnInit } from '@angular/core';
import { CuotasService } from '../../services/cuotas.service';

@Component({
  selector: 'app-cuota-alumno',
  templateUrl: './cuota-alumno.component.html',
  styleUrls: ['./cuota-alumno.component.css']
})
export class CuotaAlumnoComponent implements OnInit {
  @Input() dni!: number;

  cuotaActual: any = null;
  historial: any[] = [];
  cargando = true;

  constructor(private cuotasService: CuotasService) {}

  ngOnInit(): void {
    if (this.dni) {
      this.cargarCuotas();
    }
  }

  cargarCuotas(): void {
    this.cuotasService.getCuotasAlumno(this.dni).subscribe({
      next: (res: any) => {
        const cuotas: any[] = res.cuotas || [];
        const noPagedas = cuotas.filter((c: any) => !c.fecha_pago);
        this.cuotaActual = noPagedas.length > 0 ? noPagedas[0] : (cuotas[0] || null);
        this.historial = cuotas.slice(0, 5);
        this.cargando = false;
      },
      error: () => { this.cargando = false; }
    });
  }

  getEstadoLabel(estado: string): string {
    const map: any = {
      'AL_DIA':     '✅ Al día',
      'PENDIENTE':  '🕐 Pendiente',
      'POR_VENCER': '⚠️ Por vencer',
      'RECHAZADO':  '💀 Rechazado',
      'VENCIDA':    '🔴 Vencida',
    };
    return map[estado] || estado;
  }

  getEstadoClass(estado: string): string {
    const map: any = {
      'AL_DIA':     'estado-al-dia',
      'PENDIENTE':  'estado-pendiente',
      'POR_VENCER': 'estado-por-vencer',
      'RECHAZADO':  'estado-rechazado',
      'VENCIDA':    'estado-vencida',
    };
    return map[estado] || '';
  }

  diasRestantes(fechaVenc: string): number {
    const hoy = new Date();
    const venc = new Date(fechaVenc);
    return Math.ceil((venc.getTime() - hoy.getTime()) / (1000 * 60 * 60 * 24));
  }
}
