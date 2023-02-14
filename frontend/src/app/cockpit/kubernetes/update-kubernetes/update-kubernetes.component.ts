import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Ngxalert} from "ngx-dialogs";
import {PodsReqData} from "../pods/pods.component";
import {Observable, ReplaySubject, Subscription} from "rxjs";
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {DeployRequestData} from "../deploy-kubernetes/deploy-kubernetes.component";
import {SharedAddService} from "../../../shared-add.service";
import {CockpitService} from "../../cockpit.service";
import {BsModalService} from "ngx-bootstrap/modal";
import {Router} from "@angular/router";

@Component({
  selector: 'app-update-kubernetes',
  templateUrl: './update-kubernetes.component.html',
  styleUrls: ['./update-kubernetes.component.scss']
})
export class UpdateKubernetesComponent implements OnInit {
  // @ts-ignore
  @Input() updateAction;
  // @ts-ignore
  @Input() getAction;
  @Output() isFormValid = new EventEmitter<any>();
  @Output() submitSuccess = new EventEmitter<any>();
  isUsername: string = "monkey_d_luffy";
  requestData: any;
  responseData: any;
  disabled : boolean = true;
  // @ts-ignore
  base64Output : string;
  responseAlert:  any  =  new  Ngxalert;
  clusters: any = [];
  selectedCluster: any;
  selectedNamespace: any;
  selectedPod: any;
  namespaceReqData: any;
  namespaces: any= [];
  namespaceRes: any
  podList: any;
  // @ts-ignore
  kubernetesObjectReqData: PodsReqData[];
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
    action: this.updateAction,
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
        if(this.preSelectedNamespace != '') {
          this.kubernetesObjectReqData ={
            // @ts-ignore
            cluster_name:  this.preSelectedCluster,
            action: this.getAction,
            user_name: "monkey_d_luffy",
            metadata:{
              namespace:this.preSelectedNamespace,
              all_namespaces: "False"
            }
          }
          this.getKubernetesObjectData();
          this.loading = false;
        }
      } else {
        this.loading = true;
      }
    })
    this.updateKubernetesObjectForm();
    this.checkFormValidity();

  }

  // @ts-ignore
  selectCluster(event) {
    // @ts-ignore
    this.selectedCluster = this.clusters?.filter((cluster)=> cluster.cluster_name === event.target.value);
    this.namespaceReqData= {
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
      this.namespaceRes = res;
      this.namespaces = res.data;
    });
  }

  // @ts-ignore
  selectNamespace(event) {
    // @ts-ignore
    this.selectedNamespace = this.namespaces?.filter((namespace)=> namespace.namespace === event.target.value);
    this.kubernetesObjectReqData ={
      // @ts-ignore
      cluster_name:  this.namespaceRes.cluster_name,
      action: this.getAction,
      user_name: "monkey_d_luffy",
      metadata:{
        namespace:this.selectedNamespace[0]?.namespace,
        all_namespaces: "False"
      }
    }
    this.getKubernetesObjectData();
  }

  getKubernetesObjectData() {
    this.service.namspaceList(this.kubernetesObjectReqData).subscribe((res) => {
      this.podList= res.data;
      this.loading = true;
    });
  }

  // @ts-ignore
  selectPodName(event) {
    // @ts-ignore
    this.selectedPod = this.podList?.filter((pod) => pod.pod === event.target.value);
  }

  checkFormValidity() {
    this.createForm.statusChanges.pipe().subscribe(() => {
      this.isFormValid.emit(this.createForm.valid);
    });
  }

  updateKubernetesObjectForm() {
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
      action: this.updateAction,
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
      await this.service.updateKubernetes(this.requestData).subscribe( (res) => {
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
      console.log(this.base64Output);
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
