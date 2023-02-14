import {Component, EventEmitter, OnDestroy, OnInit, Output} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {ToastrService} from "ngx-toastr";
import {SharedAddService} from "../../../shared-add.service";
import {BsModalService} from "ngx-bootstrap/modal";
import {Router} from "@angular/router";
import {Ngxalert} from "ngx-dialogs";
import {Subscription} from "rxjs";
import {CockpitService} from "../../cockpit.service";

@Component({
  selector: 'app-existing-cluster',
  templateUrl: './existing-cluster.component.html',
  styleUrls: ['./existing-cluster.component.scss']
})
export class ExistingClusterComponent implements OnInit, OnDestroy{

  @Output() isFormValid = new EventEmitter<any>();
  @Output() submitSuccess = new EventEmitter<any>();
  requestData: any;
  responseData: any;
  submitClickSubscription$: Subscription;
  responseAlert:  any  =  new  Ngxalert;

  createForm: FormGroup = new FormGroup({
    cluster_name: new FormControl(''),
    version: new FormControl(''),
    api_server_endpoint: new FormControl(''),
    bearer_token: new FormControl(''),
    kubeconfig: new FormControl(''),
    cloud: new FormControl('')
  });

  addForm: AddRequestModel = {
    cluster_name: '',
    version: '',
    api_server_endpoint: '',
    bearer_token: '',
    kubeconfig: '',
    cloud: '',
  };
  constructor( private formBuilder: FormBuilder,
               private toast: ToastrService,
               private sharedAddService: SharedAddService,
               private modalService: BsModalService,
               private service: CockpitService,
               private _router: Router) {
    this.submitClickSubscription$ = this.sharedAddService
      .getSubmitClick()
      .subscribe(() => {
        this.saveRequestData();
      });
  }

  ngOnInit(): void {
    this.createExistingClusterForm();
    this.checkFormValidity();
  }

  checkFormValidity() {
    this.createForm.statusChanges.pipe().subscribe(() => {
      this.isFormValid.emit(this.createForm.valid);
    });
  }

  createExistingClusterForm() {
    this.createForm = this.formBuilder.group({
      cluster_name: [this.addForm.cluster_name, Validators.required ],
      version: [this.addForm.version, Validators.required],
      api_server_endpoint: [this.addForm.api_server_endpoint, Validators.required],
      bearer_token: [this.addForm.bearer_token, Validators.required],
      kubeconfig: [this.addForm.kubeconfig, Validators.required],
      cloud: [this.addForm.cloud, Validators.required]
    });
  }

  async saveRequestData() {

    this.requestData = {
      // @ts-ignore
      cluster_name: this.createForm.get('cluster_name').value,
      // @ts-ignore
      version: this.createForm.get('version').value,
      // @ts-ignore
      api_server_endpoint: this.createForm.get('api_server_endpoint').value,
      // @ts-ignore
      bearer_token: this.createForm.get('bearer_token').value,
      // @ts-ignore
      kubeconfig: this.createForm.get('kubeconfig').value,
      // @ts-ignore
      cloud: this.createForm.get('cloud').value,
    };

    if (this.requestData !== '') {
      await this.service.importCluster(this.requestData).subscribe((res) => {
        this.responseData = JSON.stringify(res, undefined, 4);
        this.sharedAddService.send(this.responseData)
        // this.responseData = res;
        // this.openSimpleAlert();
      })
      this.submitSuccess.emit(true);
      this.createForm.reset();
      // this.modalService.hide();
      this.reloadCurrentRoute();
    }
  }

  openSimpleAlert() {
    this.responseAlert.create({
      message: `message: ${this.responseData.message}\n
      status_code: ${this.responseData.status_code}\n
      cluster_name: ${this.responseData.cluster_name}\n
      version: ${this.responseData.version}`,
      type: 'M',
      customCssClass:  'custom-dialog',
    });
  }

  reloadCurrentRoute() {
    let currentUrl = this._router.url;
    this._router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
      this._router.navigate([currentUrl]);
    });
  }
  ngOnDestroy(): void {
    this.reloadCurrentRoute();
  }

}

export interface AddRequestModel {
  cluster_name: string;
  version: string;
  api_server_endpoint:string;
  bearer_token: string;
  kubeconfig: string,
  cloud: string
}
