import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VistaProfeComponent } from './vista-profe.component';

describe('VistaProfeComponent', () => {
  let component: VistaProfeComponent;
  let fixture: ComponentFixture<VistaProfeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VistaProfeComponent]
    });
    fixture = TestBed.createComponent(VistaProfeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
