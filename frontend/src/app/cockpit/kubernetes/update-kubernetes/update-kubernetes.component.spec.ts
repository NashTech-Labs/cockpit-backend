import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateKubernetesComponent } from './update-kubernetes.component';

describe('UpdateKubernetesComponent', () => {
  let component: UpdateKubernetesComponent;
  let fixture: ComponentFixture<UpdateKubernetesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdateKubernetesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateKubernetesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
