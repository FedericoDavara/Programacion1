import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  rutavisible = true;
  sidebarOpen = false;

  constructor(private router: Router) { 
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.rutavisible = event.url !== '/login';
      }
    });
  }

  toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  }

  closeSidebar() {
    this.sidebarOpen = false;
  }

  scrollToTop() {
    this.closeSidebar();
    const rutaActual = this.router.url;

    if (rutaActual === '/login') {
      this.router.navigate(['/home']).then(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  scrollToClases() {
    this.closeSidebar();
    const rutaActual = this.router.url;

    if (rutaActual === '/login') {
      this.router.navigate(['/home']).then(() => {
        const elementoDestino = document.getElementById('Clasesid');
        if (elementoDestino) {
          elementoDestino.scrollIntoView({ behavior: 'smooth' });
        }
      });
    } else {
      const elementoDestino = document.getElementById('Clasesid');
      if (elementoDestino) {
        elementoDestino.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }

  scrollToPrecio() {
    this.closeSidebar();
    const rutaActual = this.router.url;

    if (rutaActual === '/login') {
      this.router.navigate(['/home']).then(() => {
        const elementoDestino = document.getElementById('Promosid');
        if (elementoDestino) {
          elementoDestino.scrollIntoView({ behavior: 'smooth' });
        }
      });
    } else {
      const elementoDestino = document.getElementById('Promosid');
      if (elementoDestino) {
        elementoDestino.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }

  scrollToProfes() {
    this.closeSidebar();
    const rutaActual = this.router.url;

    if (rutaActual === '/login') {
      this.router.navigate(['/home']).then(() => {
        const elementoDestino = document.getElementById('Profesid');
        if (elementoDestino) {
          elementoDestino.scrollIntoView({ behavior: 'smooth' });
        }
      });
    } else {
      const elementoDestino = document.getElementById('Profesid');
      if (elementoDestino) {
        elementoDestino.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }

  scrollToContacto() {
    this.closeSidebar();
    const rutaActual = this.router.url;

    if (rutaActual === '/login') {
      this.router.navigate(['/home']).then(() => {
        const elementoDestino = document.getElementById('Contactosid');
        if (elementoDestino) {
          elementoDestino.scrollIntoView({ behavior: 'smooth' });
        }
      });
    } else {
      const elementoDestino = document.getElementById('Contactosid');
      if (elementoDestino) {
        elementoDestino.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }
}
