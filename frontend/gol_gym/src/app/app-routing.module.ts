import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { PlanificacionesComponent } from './pages/planificaciones/planificaciones.component';
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
import { authsessionGuard } from './guards/authsession.guard';
import { AdminComponent } from './pages/admin/admin.component';

const routes: Routes = [
  {path: 'home',component: HomeComponent},
  {path: 'login',component: LoginComponent},
  {path: 'clases',component: ClasesComponent},
  {path: 'planificacion',component: PlanificacionesComponent},
  {path: 'profesores',component: ProfesoresComponent},
  {path: 'registro',component: RegistroComponent},
  {path: 'usuarios',component: UsuariosComponent, canActivate:[authsessionGuard]}, 
  {path: 'vista-admin',component: VistaAdminComponent},
  {path: 'vista-profe',component: VistaProfeComponent},
  {path: 'alta-alumnoadmin',component: AltaAlumnoadminComponent},
  {path: 'alta-profesoresadmin',component: AltaProfesoresadminComponent},
  {path: 'baja-alumnoadmin',component: BajaAlumnoadminComponent},
  {path: 'baja-claseprofe',component: BajaClaseprofeComponent},
  {path: 'baja-profesoradmin',component: BajaProfesoradminComponent},
  {path: 'admin',component: AdminComponent},
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: '**', redirectTo: 'error-page'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

