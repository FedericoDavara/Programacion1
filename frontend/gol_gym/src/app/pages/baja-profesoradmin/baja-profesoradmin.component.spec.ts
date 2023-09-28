import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BajaProfesoradminComponent } from './baja-profesoradmin.component';

describe('BajaProfesoradminComponent', () => {
  let component: BajaProfesoradminComponent;
  let fixture: ComponentFixture<BajaProfesoradminComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BajaProfesoradminComponent]
    });
    fixture = TestBed.createComponent(BajaProfesoradminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
