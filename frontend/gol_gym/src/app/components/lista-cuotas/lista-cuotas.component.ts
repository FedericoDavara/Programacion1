import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CuotasService } from '../../services/cuotas.service';

@Component({
  selector: 'app-lista-cuotas',
  templateUrl: './lista-cuotas.component.html',
  styleUrls: ['./lista-cuotas.component.css']
})
export class ListaCuotasComponent implements OnInit {
  cuotas: any[] = [];
  resumen: any = {};
  filtroActivo: string = 'TODOS';
  cargando = false;
  mensajeExito = '';
  mensajeError = '';

  formNuevaCuota: FormGroup;
  mostrarFormulario = false;

  filtros = [
    { label: 'Todos', valor: 'TODOS' },
    { label: '✅ Al día', valor: 'AL_DIA' },
    { label: '⚠️ Por vencer', valor: 'POR_VENCER' },
    { label: '💀 Rechazado', valor: 'RECHAZADO' },
    { label: '🔴 Vencidas', valor: 'VENCIDA' },
  ];

  constructor(private cuotasService: CuotasService, private fb: FormBuilder) {
    this.formNuevaCuota = this.fb.group({
      alumno_dni: ['', [Validators.required, Validators.pattern('^[0-9]{7,8}$')]],
      plan: ['Street Fighter II (The World Warrior)', Validators.required],
      monto_base: ['', [Validators.required, Validators.min(1)]],
      fecha_vencimiento: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.cargarCuotas();
  }

  cargarCuotas(): void {
    this.cargando = true;
    const estado = this.filtroActivo === 'TODOS' ? undefined : this.filtroActivo;
    this.cuotasService.getCuotas(estado).subscribe({
      next: (res: any) => {
        this.cuotas = res.cuotas;
        this.resumen = res.resumen;
        this.cargando = false;
      },
      error: () => { this.cargando = false; }
    });
  }

  aplicarFiltro(valor: string): void {
    this.filtroActivo = valor;
    this.cargarCuotas();
  }

  registrarPago(id: number): void {
    if (!confirm('¿Confirmar el pago de esta cuota?')) return;
    this.cuotasService.registrarPago(id).subscribe({
      next: () => {
        this.mensajeExito = '✅ PLAYER 1 READY — Pago registrado correctamente.';
        this.cargarCuotas();
        setTimeout(() => this.mensajeExito = '', 4000);
      },
      error: (e: any) => {
        this.mensajeError = e.error?.error || 'Error al registrar el pago.';
        setTimeout(() => this.mensajeError = '', 4000);
      }
    });
  }

  crearCuota(): void {
    if (this.formNuevaCuota.invalid) return;
    const data = this.formNuevaCuota.value;
    data.alumno_dni = parseInt(data.alumno_dni);
    data.monto_base = parseFloat(data.monto_base);
    this.cuotasService.createCuota(data).subscribe({
      next: () => {
        this.mensajeExito = '🪙 INSERT COIN — Cuota creada y email enviado al alumno.';
        this.mostrarFormulario = false;
        this.formNuevaCuota.reset({ plan: 'Street Fighter II (The World Warrior)' });
        this.cargarCuotas();
        setTimeout(() => this.mensajeExito = '', 4000);
      },
      error: (e: any) => {
        this.mensajeError = e.error?.error || 'Error al crear la cuota.';
        setTimeout(() => this.mensajeError = '', 4000);
      }
    });
  }

  eliminarCuota(id: number): void {
    if (!confirm('¿Eliminar esta cuota? Esta acción no se puede deshacer.')) return;
    this.cuotasService.deleteCuota(id).subscribe({
      next: () => { this.cargarCuotas(); },
      error: () => { this.mensajeError = 'Error al eliminar la cuota.'; }
    });
  }

  procesarVencimientos(): void {
    if (!confirm('¿Procesar vencimientos? Se notificará a alumnos morosos y se suspenderán los que superaron los 3 días de gracia.')) return;
    this.cuotasService.procesarVencimientos().subscribe({
      next: (res: any) => {
        this.mensajeExito = `Procesado: ${res.procesadas} notificaciones, ${res.suspendidos} suspensiones.`;
        this.cargarCuotas();
        setTimeout(() => this.mensajeExito = '', 5000);
      },
      error: () => { this.mensajeError = 'Error al procesar vencimientos.'; }
    });
  }

  getEstadoClass(estado: string): string {
    const map: any = {
      'AL_DIA': 'estado-al-dia',
      'PENDIENTE': 'estado-pendiente',
      'POR_VENCER': 'estado-por-vencer',
      'RECHAZADO': 'estado-rechazado',
      'VENCIDA': 'estado-vencida',
    };
    return map[estado] || '';
  }

  getEstadoLabel(estado: string): string {
    const map: any = {
      'AL_DIA': '✅ Al día',
      'PENDIENTE': '🕐 Pendiente',
      'POR_VENCER': '⚠️ Por vencer',
      'RECHAZADO': '💀 Rechazado',
      'VENCIDA': '🔴 Vencida',
    };
    return map[estado] || estado;
  }
}
