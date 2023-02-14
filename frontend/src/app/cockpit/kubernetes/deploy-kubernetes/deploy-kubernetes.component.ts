import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Ngxalert} from "ngx-dialogs";
import {Observable, ReplaySubject, Subscription} from "rxjs";
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {SharedAddService} from "../../../shared-add.service";
import {CockpitService} from "../../cockpit.service";
import {BsModalService} from "ngx-bootstrap/modal";
import {Router} from "@angular/router";

@Component({
  selector: 'app-deploy-kubernetes',
  templateUrl: './deploy-kubernetes.component.html',
  styleUrls: ['./deploy-kubernetes.component.scss']
})
export class DeployKubernetesComponent implements OnInit {
  @Output() isFormValid = new EventEmitter<any>();
  @Output() submitSuccess = new EventEmitter<any>();
  // @ts-ignore
  @Input() createAction;
  // @ts-ignore
  @Input() title;
  requestData: any;
  responseData: any;
  isUsername: string = "monkey_d_luffy";
  // @ts-ignore
  base64Output : string;
  responseAlert:  any  =  new  Ngxalert;
  clusters: any = [];
  selectedCluster: any;
  selectedNamespace: any;
  namespaceReqData: any;
  namespaces: any= [];
  // @ts-ignore
  subscription: Subscription;
  submitClickSubscription$: Subscription;
  createForm: FormGroup = new FormGroup({
    cluster_name: new FormControl(''),
    namespace: new FormControl(''),
    manifest: new FormControl(''),
    k8s_object_name: new FormControl('')
  });


  addForm: DeployRequestData = {
    cluster_name: '',
    // @ts-ignore
    action: this.createAction,
    user_name: 'monkey_d_luffy',
    metadata: {
      namespace: '',
      manifest: '',
      k8s_object_name: '',
    }
  };
  preSelectedCluster: string = '';
  preSelectedNamespace: string = '';
  loading : boolean = false;

  constructor(private sharedAddService: SharedAddService,
              private formBuilder: FormBuilder,
              private service: CockpitService,
              private modalService: BsModalService,
              private _router: Router) {
    this.submitClickSubscription$ = this.sharedAddService
      .getSubmitClick()
      .subscribe(() => {
        this.saveRequestData();
      });
  }

  ngOnInit(): void {
    this.subscription = this.sharedAddService.names$.subscribe(val=>{
      console.log(val);
      this.preSelectedCluster = val.cul;
      this.preSelectedNamespace = val.na[0]?.namespace;
      this.getClusterList();
      if (this.preSelectedCluster != '') {
        this.namespaceReqData = {
          cluster_name: val.cul,
          action:"get-namespace",
          user_name: "monkey_d_luffy",
          metadata:{
            namespace:"default",
            all_namespaces: "True"
          }
        }
        this.getNamespaceList();
        this.loading = false;
      }
      else {
        this.loading = true;
      }
    })
    this.deployKubernetesObjectForm();
    this.checkFormValidity();

  }

  // @ts-ignore
  selectCluster(event) {
    // @ts-ignore
    this.selectedCluster = this.clusters?.filter((cluster) => cluster.cluster_name === event.target.value);
    console.log(this.selectedCluster);
    this.namespaceReqData = {
      cluster_name: this.selectedCluster[0]?.cluster_name,
      action:"get-namespace",
      user_name: "monkey_d_luffy",
      metadata:{
        namespace:"default",
        all_namespaces: "True"
      }
    }
    this.getNamespaceList();
  }

  getClusterList() {
    this.service.getImportedCluster().subscribe((res) => {
      this.clusters = res.clusters;
    });

  }

  getNamespaceList() {
    this.service.namspaceList(this.namespaceReqData).subscribe((res) => {
      this.namespaces = res.data;
      this.loading = true;
    });
  }

  // @ts-ignore
  selectNamespace(event) {
    // @ts-ignore
    this.selectedNamespace = this.namespaces?.filter((namespace)=> namespace.namespace === event.target.value);
  }


  checkFormValidity() {
    this.createForm.statusChanges.pipe().subscribe(() => {
      this.isFormValid.emit(this.createForm.valid);
    });
  }

  deployKubernetesObjectForm() {
    this.createForm = this.formBuilder.group({
      cluster_name: [this.addForm.cluster_name, Validators.required ],
      namespace: [this.addForm.metadata.namespace, Validators.required],
      manifest: [this.addForm.metadata.manifest, Validators.required],
      k8s_object_name: [this.addForm.metadata.k8s_object_name, Validators.required]
    });
  }

  async saveRequestData() {

    this.requestData = {
      // @ts-ignore
      cluster_name: this.createForm.get('cluster_name').value,
      // @ts-ignore
      action: this.createAction,
      // @ts-ignore
      user_name: this.isUsername,
      // @ts-ignore
      metadata: {
        // @ts-ignore
        namespace: this.createForm.get('namespace').value,
        // @ts-ignore
        manifest: this.base64Output,
        // @ts-ignore
        k8s_object_name: this.createForm.get('k8s_object_name').value,
      }
    };

    if (this.requestData !== '') {
      await this.service.createKubernetes(this.requestData).subscribe((res) => {
        this.responseData = JSON.stringify(res.data, undefined, 4);
        this.sharedAddService.send(this.responseData)
      })
      this.submitSuccess.emit(true);
      this.createForm.reset();
    }

  }

  // @ts-ignore
  onFileSelected(event) {
    this.convertFile(event.target.files[0]).subscribe(base64 => {
      this.base64Output = base64;
    });
  }
  convertFile(file : File) : Observable<string> {
    const result = new ReplaySubject<string>(1);
    const reader = new FileReader();
    reader.readAsBinaryString(file);
    // @ts-ignore
    reader.onload = (event) => result.next(btoa(event.target.result.toString()));
    return result;
  }

}

export interface DeployRequestData {
  cluster_name: string;
  action: string;
  user_name:string;
  metadata: MetaData;
}

export interface MetaData {
  namespace: string,
  manifest: string,
  k8s_object_name: string
}
