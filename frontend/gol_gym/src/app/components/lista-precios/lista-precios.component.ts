import { Component, OnInit } from '@angular/core';
import { PreciosService } from 'src/app/services/precios.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-lista-precios',
  templateUrl: './lista-precios.component.html',
  styleUrls: ['./lista-precios.component.css']
})
export class ListaPreciosComponent implements OnInit {
  newPrecioForm!: FormGroup;
  editPrecioForm!: FormGroup;
  arrayPrecios: any;
  selectedRole = localStorage.getItem('role');
  precioAEditar: any = {};

  constructor(
    private precioService: PreciosService,
    private formBuilder: FormBuilder
  ) {
    this.newPrecioForm = this.formBuilder.group({
      nombre: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(50)]],
      precio: ['', [Validators.required]],
      descripcion: ['']
    });

    this.editPrecioForm = this.formBuilder.group({
      id: [''],
      nombre: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(50)]],
      precio: ['', [Validators.required]],
      descripcion: ['']
    });
  }

  ngOnInit(): void {
    this.cargarPrecios();
  }

  cargarPrecios() {
    this.precioService.getPrecios().subscribe((data: any) => {
      this.arrayPrecios = data;
    });
  }

  crearPrecio() {
    if (this.newPrecioForm.valid) {
      this.precioService.createPrecio(this.newPrecioForm.value).subscribe(
        (data: any) => {
          this.cargarPrecios();
          this.newPrecioForm.reset();
        }
      );
    }
  }

  initFormForEdit(precio: any) {
    this.precioAEditar = precio;
    this.editPrecioForm.setValue({
      id: precio.id,
      nombre: precio.nombre,
      precio: precio.precio,
      descripcion: precio.descripcion || ''
    });
  }

  editarPrecio() {
    if (this.editPrecioForm.valid) {
      const id = this.editPrecioForm.value.id;
      const data = this.editPrecioForm.value;
      this.precioService.updatePrecio(id, data).subscribe(
        (data: any) => {
          this.cargarPrecios();
        }
      );
    }
  }

  prepareDelete(precio: any) {
    this.precioAEditar = precio;
  }

  borrarPrecio() {
    const id = this.precioAEditar.id;
    this.precioService.deletePrecio(id).subscribe(
      (data: any) => {
        this.cargarPrecios();
      }
    );
  }
}
