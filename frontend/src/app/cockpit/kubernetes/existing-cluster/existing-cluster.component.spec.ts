import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExistingClusterComponent } from './existing-cluster.component';

describe('ExistingClusterComponent', () => {
  let component: ExistingClusterComponent;
  let fixture: ComponentFixture<ExistingClusterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExistingClusterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ExistingClusterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
