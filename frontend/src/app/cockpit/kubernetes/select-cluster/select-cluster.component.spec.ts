import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectClusterComponent } from './select-cluster.component';

describe('SelectClusterComponent', () => {
  let component: SelectClusterComponent;
  let fixture: ComponentFixture<SelectClusterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SelectClusterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectClusterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
