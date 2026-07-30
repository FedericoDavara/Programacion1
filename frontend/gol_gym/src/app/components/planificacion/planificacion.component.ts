import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute, Params } from '@angular/router';
import { PlanificacionService } from 'src/app/services/planificacion.service';
import { UsuariosService } from 'src/app/services/usuarios.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-planificacion',
  templateUrl: './planificacion.component.html',
  styleUrls: ['./planificacion.component.css']
})
export class PlanificacionComponent implements OnInit {
  planifForm!: FormGroup
  selectedRole = localStorage.getItem('role');

  UserPlanif: any = null;

  DataPlanif: any = {
    "descripcion": null,
    "fecha": null,
    "lunes": null,
    "martes": null,
    "miercoles": null,
    "jueves": null,
    "viernes": null,
    "sabado": null,
    "alumno_dni": null,
    "profesor_dni": null
  };

  private parametrosOcultos: any;

  PlanifID: number = 0;

  userDNI: number = 0;
  perfilDni: number = 0;

  allProf: any[] = [];

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private planificacionService: PlanificacionService,
    private usuariosService: UsuariosService,
    private formBuilder: FormBuilder,
  ) {
    this.planifForm = this.formBuilder.group({
      descripcion: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(200)]],
      fecha: ['', [Validators.required]],
      lunes: ['', [Validators.maxLength(1000)]],
      martes: ['', [Validators.maxLength(1000)]],
      miercoles: ['', [Validators.maxLength(1000)]],
      jueves: ['', [Validators.maxLength(1000)]],
      viernes: ['', [Validators.maxLength(1000)]],
      sabado: ['', [Validators.maxLength(1000)]],
      alumno_dni: ['', [Validators.required, Validators.pattern(/^[0-9]+$/)]],
      profesor_dni: ['', [Validators.required]],
    });
  }

  ngOnInit(): void {
    this.userDNI = this.usuariosService.getUserDNIFromToken() || 0;
    this.parametrosOcultos = history.state;

    this.route.params.subscribe((params: Params) => {
      this.perfilDni = this.parametrosOcultos.dni;
      // Establecer alumno_dni automáticamente una vez que tenemos perfilDni
      this.planifForm.patchValue({ alumno_dni: Number(this.perfilDni) });
    });
    
    this.usuariosService.getAllProf().subscribe(
      (data) => {
        this.allProf = data;
      },
      (error) => {
        console.error('Error al obtener datos de profesores:', error);
      }
    );

    this.cargarPlanificacion();
  }

  private cargarPlanificacion(): void {
    this.planificacionService.getPlanif(this.perfilDni).subscribe(
      (userPlanif) => {
        this.UserPlanif = userPlanif;

        if (Array.isArray(userPlanif) && userPlanif.length > 0) {
          const planif = userPlanif[0];
          this.planifForm.patchValue({
            descripcion: planif.descripcion,
            fecha: planif.fecha,
            lunes: planif.lunes || '',
            martes: planif.martes || '',
            miercoles: planif.miercoles || '',
            jueves: planif.jueves || '',
            viernes: planif.viernes || '',
            sabado: planif.sabado || '',
            alumno_dni: planif.alumno.dni,
            profesor_dni: planif.profesor.dni
          });

          this.PlanifID = planif.id
          this.DataPlanif = {
            "descripcion": planif.descripcion,
            "fecha": planif.fecha,
            "lunes": planif.lunes,
            "martes": planif.martes,
            "miercoles": planif.miercoles,
            "jueves": planif.jueves,
            "viernes": planif.viernes,
            "sabado": planif.sabado,
            "alumno_dni": planif.alumno.dni,
            "profesor_dni": planif.profesor.dni
          };
        } else {
          // No hay planificación existente, inicializar DataPlanif como objeto vacío
          this.UserPlanif = null;
          this.DataPlanif = {
            "descripcion": null,
            "fecha": null,
            "lunes": null,
            "martes": null,
            "miercoles": null,
            "jueves": null,
            "viernes": null,
            "sabado": null,
            "alumno_dni": null,
            "profesor_dni": null
          };
        }
      },
      (error) => {
        console.error('Error al obtener planificación:', error);
        this.UserPlanif = null;
        // En caso de error, también inicializar DataPlanif
        this.DataPlanif = {
          "descripcion": null,
          "fecha": null,
          "lunes": null,
          "martes": null,
          "miercoles": null,
          "jueves": null,
          "viernes": null,
          "sabado": null,
          "alumno_dni": null,
          "profesor_dni": null
        };
      }
    );
  }

  crearPlanificacion(dataPLanif: any = {}) {
    this.planificacionService.createPlanif(dataPLanif).subscribe(
      (response) => {
        this.cargarPlanificacion();
      },
      (error) => {
        console.error('Error al crear planificación:', error);
      }
    );
  }
  editarPlanificacion(dataPlanif: any = {}) {
    this.planificacionService.updatePlanif(this.PlanifID, dataPlanif).subscribe(
      (response) => {
        this.cargarPlanificacion();
      },
      (error) => {
        console.error('Error al actualizar planificación:', error);
      }
    );
  }

  eliminarPlanificacion() {
    this.planificacionService.deletePlanif(this.PlanifID).subscribe(
      (response) => {
        this.cargarPlanificacion();
      }
    );
  }
  submit() {
    if (this.planifForm.valid) {
      const datosParaEnviar = {
        ...this.planifForm.value,
        alumno_dni: Number(this.planifForm.value.alumno_dni),
        profesor_dni: Number(this.planifForm.value.profesor_dni)
      };

      if (this.shouldEditPlanif()) {
        this.editarPlanificacion(datosParaEnviar);
      } else {
        this.crearPlanificacion(datosParaEnviar);
      }
    } else {
      alert('Formulario inválido. Revisa los campos marcados en rojo.');
    }
  }
  
  
  shouldEditPlanif(): boolean {
    return this.UserPlanif && Array.isArray(this.UserPlanif) && this.UserPlanif.length > 0;
  }

  borrarPlanifiacacion(){
    this.eliminarPlanificacion();
  }

  verPerfil(dni: number) {
    const parametrosOcultos = {
      dni: dni
    };
    this.router.navigate(['/vPerfil'], { state: parametrosOcultos });
  }
}
