import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import jwtDecode from 'jwt-decode';

export const authsessionGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');

  if (!token) {
    router.navigateByUrl('home');
    return false;
  }

  try {
    const { exp } = jwtDecode<{ exp: number }>(token);
    if (exp && Date.now() >= exp * 1000) {
      localStorage.clear();
      router.navigateByUrl('home');
      return false;
    }
  } catch {
    localStorage.clear();
    router.navigateByUrl('home');
    return false;
  }

  return true;
};
