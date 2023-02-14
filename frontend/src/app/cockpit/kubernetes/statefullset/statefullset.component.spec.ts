import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatefullsetComponent } from './statefullset.component';

describe('StatefullsetComponent', () => {
  let component: StatefullsetComponent;
  let fixture: ComponentFixture<StatefullsetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StatefullsetComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StatefullsetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
