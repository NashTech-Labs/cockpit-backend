import { TestBed } from '@angular/core/testing';

import { CockpitService } from './cockpit.service';

describe('CockpitService', () => {
  let service: CockpitService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CockpitService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
