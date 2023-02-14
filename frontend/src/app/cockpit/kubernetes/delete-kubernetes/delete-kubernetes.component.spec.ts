import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteKubernetesComponent } from './delete-kubernetes.component';

describe('DeleteKubernetesComponent', () => {
  let component: DeleteKubernetesComponent;
  let fixture: ComponentFixture<DeleteKubernetesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DeleteKubernetesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteKubernetesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
