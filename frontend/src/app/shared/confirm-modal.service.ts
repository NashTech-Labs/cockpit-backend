import { Injectable } from '@angular/core';
import { BsModalRef, BsModalService } from 'ngx-bootstrap/modal';
import { ConfirmModalComponent } from './confirm-modal/confirm-modal.component';

@Injectable({
  providedIn: 'root'
})
export class ConfirmModalService {

  // @ts-ignore
  modalRef: BsModalRef;
  constructor(private modalService: BsModalService) {}

  confirm(options: any): Promise<any> {
    return new Promise((resolve, reject) => {
      this.modalRef = this.modalService.show(ConfirmModalComponent);
      this.modalRef.content.title = options.title;
      this.modalRef.content.remark =  options.remark;
      this.modalRef.content.confirmLabel = options.confirmLabel;
      this.modalRef.content.declineLabel = options.declineLabel;
      this.modalRef.content.onClose.subscribe((result: boolean) => {
        resolve(result);
      });
    });
  }
}
