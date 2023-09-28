import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BajaClaseprofeComponent } from './baja-claseprofe.component';

describe('BajaClaseprofeComponent', () => {
  let component: BajaClaseprofeComponent;
  let fixture: ComponentFixture<BajaClaseprofeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BajaClaseprofeComponent]
    });
    fixture = TestBed.createComponent(BajaClaseprofeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
