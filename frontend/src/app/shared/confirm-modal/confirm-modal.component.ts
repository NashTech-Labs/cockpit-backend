import { Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal';
import { Subject } from 'rxjs';
@Component({
  selector: 'app-confirm-modal',
  templateUrl: './confirm-modal.component.html',
  styleUrls: ['./confirm-modal.component.scss']
})
export class ConfirmModalComponent implements OnInit {
  // @ts-ignore
  public onClose: Subject<boolean>;
  // @ts-ignore
  title: string;
  public remark:any;
  test:any;
  // @ts-ignore
  confirmLabel: string;
  // @ts-ignore
  declineLabel: string;
  // @ts-ignore
  @ViewChild('dialog') dialog:ElementRef;

  constructor(public bsModalRef: BsModalRef) {}

  public ngOnInit(): void {
    this.onClose = new Subject();
  }

  confirm() {
    this.onClose.next(true);
    this.bsModalRef.hide();
    this.test=this.dialog.nativeElement.value;
    localStorage.setItem('remark', String(this.test));
  }

  decline() {
    this.onClose.next(false);
    this.bsModalRef.hide();
  }
}

