import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { ClasesComponent } from './pages/clases/clases.component';
import { ProfesoresComponent } from './pages/profesores/profesores.component';
import { AltaAlumnoadminComponent } from './pages/alta-alumnoadmin/alta-alumnoadmin.component';
import { AltaProfesoresadminComponent } from './pages/alta-profesoresadmin/alta-profesoresadmin.component';
import { BajaProfesoradminComponent } from './pages/baja-profesoradmin/baja-profesoradmin.component';
import { BajaAlumnoadminComponent } from './pages/baja-alumnoadmin/baja-alumnoadmin.component';
import { BajaClaseprofeComponent } from './pages/baja-claseprofe/baja-claseprofe.component';
import { RegistroComponent } from './pages/registro/registro.component';
import { UsuariosComponent } from './pages/usuarios/usuarios.component';
import { VistaAdminComponent } from './pages/vista-admin/vista-admin.component';
import { VistaProfeComponent } from './pages/vista-profe/vista-profe.component';
import { ErrorPageComponent } from './pages/error-page/error-page.component';
import { NavComponent } from './components/nav/nav.component';
import { PlanificacionesComponent } from './pages/planificaciones/planificaciones.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    ClasesComponent,
    ProfesoresComponent,
    AltaAlumnoadminComponent,
    AltaProfesoresadminComponent,
    BajaProfesoradminComponent,
    BajaAlumnoadminComponent,
    BajaClaseprofeComponent,
    RegistroComponent,
    UsuariosComponent,
    VistaAdminComponent,
    VistaProfeComponent,
    ErrorPageComponent,
    NavComponent,
    PlanificacionesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
