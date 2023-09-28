import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BajaAlumnoadminComponent } from './baja-alumnoadmin.component';

describe('BajaAlumnoadminComponent', () => {
  let component: BajaAlumnoadminComponent;
  let fixture: ComponentFixture<BajaAlumnoadminComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BajaAlumnoadminComponent]
    });
    fixture = TestBed.createComponent(BajaAlumnoadminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
