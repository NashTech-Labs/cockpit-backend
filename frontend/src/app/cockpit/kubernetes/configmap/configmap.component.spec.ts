import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfigmapComponent } from './configmap.component';

describe('ConfigmapComponent', () => {
  let component: ConfigmapComponent;
  let fixture: ComponentFixture<ConfigmapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ConfigmapComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfigmapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
