import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AltaAlumnoadminComponent } from './alta-alumnoadmin.component';

describe('AltaAlumnoadminComponent', () => {
  let component: AltaAlumnoadminComponent;
  let fixture: ComponentFixture<AltaAlumnoadminComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AltaAlumnoadminComponent]
    });
    fixture = TestBed.createComponent(AltaAlumnoadminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
