import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { NavcloseComponent } from './components/navclose/navclose.component';
import { PlanificacionComponent } from './components/planificacion/planificacion.component';
import { VistaPlanificacionComponent } from './pages/vista-planificacion/vista-planificacion.component';
import { ListaUsuariosComponent } from './components/lista-usuarios/lista-usuarios.component';
import { PerfilComponent } from './components/perfil/perfil.component';
import { VistaPerfilComponent } from './pages/vista-perfil/vista-perfil.component';
import { VistaInicioComponent } from './pages/vista-inicio/vista-inicio.component';
import { VistaErrorComponent } from './pages/vista-error/vista-error.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ClaseComponent } from './components/clase/clase.component';
import { ListaClasesComponent } from './components/lista-clases/lista-clases.component';
import { ListaPreciosComponent } from './components/lista-precios/lista-precios.component';
import { ListaProfesoresComponent } from './components/lista-profesores/lista-profesores.component';
import { ListaCuotasComponent } from './components/lista-cuotas/lista-cuotas.component';
import { CuotaAlumnoComponent } from './components/cuota-alumno/cuota-alumno.component';
import { DatePipe } from '@angular/common';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    NavbarComponent,
    NavcloseComponent,
    PlanificacionComponent,
    VistaPlanificacionComponent,
    PerfilComponent,
    VistaPerfilComponent,
    VistaInicioComponent,
    ListaUsuariosComponent,
    VistaErrorComponent,
    ClaseComponent,
    ListaClasesComponent,
    ListaPreciosComponent,
    ListaProfesoresComponent,
    ListaCuotasComponent,
    CuotaAlumnoComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }