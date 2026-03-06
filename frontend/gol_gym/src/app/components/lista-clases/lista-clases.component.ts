import { Component, OnInit } from '@angular/core';
import { ClasesService } from 'src/app/services/clases.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-lista-clases',
  templateUrl: './lista-clases.component.html',
  styleUrls: ['./lista-clases.component.css']
})
export class ListaClasesComponent implements OnInit {
  newClaseForm!: FormGroup;
  editClaseForm!: FormGroup;
  arrayClases: any;
  selectedRole = localStorage.getItem('role');
  diasSemana: string[] = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
  claseAEditar: any = {};

  constructor(
    private claseService: ClasesService,
    private formBuilder: FormBuilder
  ) {
    this.newClaseForm = this.formBuilder.group({
      nombre: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(50), Validators.pattern(/^[a-zA-ZÀ-ÿ\s0-9]+$/)]],
      dia: ['', Validators.required],
      horario: ['', [Validators.required, Validators.pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9](-([0-1]?[0-9]|2[0-3]):[0-5][0-9])?$/)]],
      imagen: ['']
    });

    this.editClaseForm = this.formBuilder.group({
      id: [''],
      nombre: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(50), Validators.pattern(/^[a-zA-ZÀ-ÿ\s0-9]+$/)]],
      dia: ['', Validators.required],
      horario: ['', [Validators.required, Validators.pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9](-([0-1]?[0-9]|2[0-3]):[0-5][0-9])?$/)]],
      imagen: ['']
    });
  }

  ngOnInit(): void {
    this.cargarClases();
  }

  cargarClases() {
    this.claseService.getClases().subscribe((data: any) => {
      this.arrayClases = data;
    });
  }

  crearClase() {
    if (this.newClaseForm.valid) {
      const claseData = {
        ...this.newClaseForm.value,
        profesores: []
      };
      this.claseService.createClase(claseData).subscribe(
        (data: any) => {
          this.cargarClases();
          this.newClaseForm.reset();
        }
      );
    }
  }

  initFormForEdit(clase: any) {
    this.claseAEditar = clase;
    this.editClaseForm.setValue({
      id: clase.id,
      nombre: clase.nombre,
      dia: clase.dia,
      horario: clase.horario,
      imagen: clase.imagen || ''
    });
  }

  editarClase() {
    if (this.editClaseForm.valid) {
      const id = this.editClaseForm.value.id;
      const data = this.editClaseForm.value;
      this.claseService.updateClase(id, data).subscribe(
        (data: any) => {
          this.cargarClases();
        }
      );
    }
  }

  prepareDelete(clase: any) {
    this.claseAEditar = clase;
  }

  borrarClase() {
    const id = this.claseAEditar.id;
    this.claseService.deleteClase(id).subscribe(
      (data: any) => {
        this.cargarClases();
      }
    );
  }
}
