import {Component, OnInit, TemplateRef} from '@angular/core';
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {SharedAddService} from "../../../shared-add.service";
import {FormControl} from "@angular/forms";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-cluster',
  templateUrl: './cluster.component.html',
  styleUrls: ['./cluster.component.scss']
})
export class ClusterComponent implements OnInit {
  // @ts-ignore
  knoldersReputationList: AuthorModel[];
  searchBar = new FormControl('');
  // @ts-ignore
  private modalRef: BsModalRef;
  formValid:boolean = false;
  tableHeading: TableHeaderModel[] = [
    { title: 'CLUSTER NAME' },
    { title: 'VERSION' },
    { title: 'API SERVER ENDPOINT' },
  ];
  subscription: Subscription;
  res: any;

  constructor(private modalService: BsModalService,
              private sharedAddService: SharedAddService,) {
    this.subscription =  sharedAddService.subj$.subscribe(val=>{
      console.log(val)
      this.res = val;
    })
  }

  ngOnInit(): void {
  }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template, {
      animated: true,
      class:'right-modal',
    });
  }

  onSubmitSuccess(success: any) {
    if (success) {
      this.sharedAddService.sendViewClick();
    }
  }

  submitForm() {
    this.sharedAddService.sendSubmitClick();
  }

  cancelForm() {
    this.modalService.hide();
  }

  // @ts-ignore
  onFormValid(valid){
    this.formValid = valid;
  }

}
export interface TableHeaderModel {
  title: string;
}

export interface AuthorModel {
  id: number;
  cluster_name: string;
  version: string;
  api_server_endpoint: string;
}
