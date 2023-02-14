import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DaemonsetComponent } from './daemonset.component';

describe('DaemonsetComponent', () => {
  let component: DaemonsetComponent;
  let fixture: ComponentFixture<DaemonsetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DaemonsetComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DaemonsetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
