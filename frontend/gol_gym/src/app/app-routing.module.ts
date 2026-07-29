  import { NgModule } from '@angular/core';
  import { RouterModule, Routes } from '@angular/router';
  import { HomeComponent } from './pages/home/home.component';
  import { LoginComponent } from './pages/login/login.component';
  import { PanelAdminComponent } from './pages/panel-admin/panel-admin.component';
  import { VistaPerfilComponent } from './pages/vista-perfil/vista-perfil.component';
  import { VistaPlanificacionComponent } from './pages/vista-planificacion/vista-planificacion.component';
  import { VistaErrorComponent } from './pages/vista-error/vista-error.component';
  import { authsessionGuard } from './guards/authsession.guard';
  import { ListaUsuariosComponent } from './components/lista-usuarios/lista-usuarios.component';
  import { ListaCuotasComponent } from './components/lista-cuotas/lista-cuotas.component';
  import { ListaClasesComponent } from './components/lista-clases/lista-clases.component';
  import { ListaPreciosComponent } from './components/lista-precios/lista-precios.component';
  import { ListaProfesoresComponent } from './components/lista-profesores/lista-profesores.component';

  const routes: Routes = [
    { path: 'home', component: HomeComponent },
    { path: 'login', component: LoginComponent },
    {
      path: 'vInicio',
      component: PanelAdminComponent,
      canActivate: [authsessionGuard],
      children: [
        { path: '', redirectTo: 'usuarios', pathMatch: 'full' },
        { path: 'usuarios', component: ListaUsuariosComponent },
        { path: 'cuotas', component: ListaCuotasComponent },
        { path: 'clases', component: ListaClasesComponent },
        { path: 'precios', component: ListaPreciosComponent },
        { path: 'profesores', component: ListaProfesoresComponent },
      ]
    },
    { path: 'vPerfil', component: VistaPerfilComponent, canActivate:[authsessionGuard] },
    { path: 'vPlanif', component: VistaPlanificacionComponent, canActivate:[authsessionGuard] },
    { path: 'vError', component: VistaErrorComponent },
    { path: '', redirectTo: "/home", pathMatch: "full" },
    { path: '**', redirectTo: 'vError' },
  ];

  @NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
  })
  export class AppRoutingModule { }