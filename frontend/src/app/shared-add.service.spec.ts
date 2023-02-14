import { TestBed } from '@angular/core/testing';

import { SharedAddService } from './shared-add.service';

describe('SharedAddService', () => {
  let service: SharedAddService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SharedAddService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
