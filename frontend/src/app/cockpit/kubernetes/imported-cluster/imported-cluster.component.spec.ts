import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportedClusterComponent } from './imported-cluster.component';

describe('ImportedClusterComponent', () => {
  let component: ImportedClusterComponent;
  let fixture: ComponentFixture<ImportedClusterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImportedClusterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImportedClusterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
