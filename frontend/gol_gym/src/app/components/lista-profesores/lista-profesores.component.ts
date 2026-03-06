import { Component, OnInit } from '@angular/core';
import { UsuariosService } from 'src/app/services/usuarios.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-lista-profesores',
  templateUrl: './lista-profesores.component.html',
  styleUrls: ['./lista-profesores.component.css']
})
export class ListaProfesoresComponent implements OnInit {
  arrayProfes: any[] = [];
  selectedRole = localStorage.getItem('role');
  editProfeForm!: FormGroup;
  profeAEditar: any = {};

  constructor(
    private usuariosService: UsuariosService,
    private formBuilder: FormBuilder
  ) {
    this.editProfeForm = this.formBuilder.group({
      dni: [''],
      foto: [''],
      descripcion: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(250)]]
    });
  }

  ngOnInit(): void {
    this.cargarProfesores();
  }

  cargarProfesores() {
    this.usuariosService.getAllProf().subscribe((data: any) => {
      this.arrayProfes = data;
    });
  }

  initFormForEdit(profe: any) {
    this.profeAEditar = profe;
    this.editProfeForm.setValue({
      dni: profe.dni,
      foto: profe.foto || '',
      descripcion: profe.descripcion || ''
    });
  }

  editarProfe() {
    if (this.editProfeForm.valid) {
      const dni = this.editProfeForm.value.dni;
      const data = {
        foto: this.editProfeForm.value.foto,
        descripcion: this.editProfeForm.value.descripcion
      };
      this.usuariosService.updateUserProf(dni, data).subscribe(
        (data: any) => {
          this.cargarProfesores();
        }
      );
    }
  }
}
