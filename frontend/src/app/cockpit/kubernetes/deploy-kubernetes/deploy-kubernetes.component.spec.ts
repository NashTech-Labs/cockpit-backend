import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeployKubernetesComponent } from './deploy-kubernetes.component';

describe('DeployKubernetesComponent', () => {
  let component: DeployKubernetesComponent;
  let fixture: ComponentFixture<DeployKubernetesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DeployKubernetesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DeployKubernetesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
