import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ModalModule } from 'ngx-bootstrap/modal';
import { ConfirmModalComponent } from './confirm-modal.component';
import { ConfirmModalService } from '../confirm-modal.service';

@NgModule({
  declarations: [ConfirmModalComponent],
  imports: [
    CommonModule,
    ModalModule.forRoot()
  ],
  exports:[ConfirmModalComponent],
  providers:[ConfirmModalService]
})
export class ConfirmModalModule { }
