import { TestBed } from '@angular/core/testing';
import { BsModalRef, BsModalService, ModalModule } from 'ngx-bootstrap/modal';

import { ConfirmModalService } from './confirm-modal.service';

describe('ConfirmModalService', () => {
  let service: ConfirmModalService;
  let modalService: BsModalService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ ModalModule.forRoot()],
      providers: [ BsModalRef]
    });
    service = TestBed.inject(ConfirmModalService);
    modalService = TestBed.inject(BsModalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
