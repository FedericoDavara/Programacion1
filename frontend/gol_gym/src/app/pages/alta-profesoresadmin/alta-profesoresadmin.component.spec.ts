import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AltaProfesoresadminComponent } from './alta-profesoresadmin.component';

describe('AltaProfesoresadminComponent', () => {
  let component: AltaProfesoresadminComponent;
  let fixture: ComponentFixture<AltaProfesoresadminComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AltaProfesoresadminComponent]
    });
    fixture = TestBed.createComponent(AltaProfesoresadminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
