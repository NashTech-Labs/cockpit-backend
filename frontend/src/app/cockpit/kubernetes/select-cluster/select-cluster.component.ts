import {Component, OnInit, TemplateRef} from '@angular/core';
import {CockpitService} from "../../cockpit.service";
import {Router} from "@angular/router";
import {SharedAddService} from "../../../shared-add.service";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-select-cluster',
  templateUrl: './select-cluster.component.html',
  styleUrls: ['./select-cluster.component.scss']
})
export class SelectClusterComponent implements OnInit {
  tableOffset: any;
  selectedCluster: any;
  selectedNamespace: any;
  clusters: any = [];
  namespaces: any= [];
  namespaceRes: any
  namespaceReqData: any;
  res: any;
  // @ts-ignore
  sendData: SendData;
  // @ts-ignore
  private modalRef: BsModalRef;
  formValid:boolean = false;
  cul: any;
  na: any;
  subscription: Subscription;
  title : string = 'title';
  createAction : string = '';
  getAction : string = '';
  updateAction : string = '';
  deleteAction : string = '';


  constructor(private sharedAddService: SharedAddService,
              private service: CockpitService,
              private router: Router,
              private modalService: BsModalService,) {
    this.subscription =  sharedAddService.subj$.subscribe(val=>{
      this.res = val;
    })
  }

  ngOnInit(): void {
    this.getClusterList();
  }

  //@ts-ignore
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
    this.tableOffset = 0;
  }

  getClusterList() {
    this.service.getImportedCluster().subscribe((res) => {
      this.clusters = res.clusters;
    });
  }

  //@ts-ignore
  selectNamespace(event) {
    // @ts-ignore
    this.selectedNamespace = this.namespaces?.filter((namespace)=> namespace.namespace === event.target.value);
    this.sendData = {
     cul : this.namespaceRes.cluster_name,
      na: this.selectedNamespace,
    }
    // @ts-ignore
    this.sharedAddService.sendName(this.sendData);
    this.tableOffset = 0;
  }

  getNamespaceList() {
    this.service.namspaceList(this.namespaceReqData).subscribe((res) => {
      this.namespaceRes = res;
      this.namespaces = res.data;
    });
  }

  refresh() {
    // @ts-ignore
    this.sharedAddService.sendName(this.sendData);
  }

  submitForm() {
    this.sharedAddService.sendSubmitClick();
  }

  reloadCurrentRoute() {
    this.sendData = {
      cul : '',
      na: ''
    }
    // @ts-ignore
    this.sharedAddService.sendName(this.sendData);
    let currentUrl = this.router.url;
    this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
      this.router.navigate([currentUrl]);
    });
  }

  // @ts-ignore
  onFormValid(valid){
    this.formValid = valid;
  }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template, {
      animated: true,
      class:'right-modal',
    });
  }

  cancelForm() {
    this.modalService.hide();
  }

  action(){
    let currentUrl = this.router.url;
    if(currentUrl == '/cockpit/kubernetes/pods'){
      this.title = 'Pod'
      this.createAction = "create-pod";
      this.getAction= "get-pod";
      this.updateAction = "update-pod"
      this.deleteAction = "delete-pod"
    } else if (currentUrl == '/cockpit/kubernetes/deployments'){
      this.title = 'Deployment'
      this.createAction = "create-deployment";
      this.getAction= "get-deployment";
      this.updateAction = "update-deployment"
      this.deleteAction = "delete-deployment"
    } else if (currentUrl == '/cockpit/kubernetes/secret'){
      this.title = 'Secret'
      this.createAction = "create-secret";
      this.getAction= "get-secret";
      this.updateAction = "update-secret"
      this.deleteAction = "delete-secret"
    } else if (currentUrl == '/cockpit/kubernetes/cronjob'){
      this.title = 'Cronjob'
      this.createAction = "create-cronjob";
      this.getAction= "get-cronjob";
      this.updateAction = "update-cronjob"
      this.deleteAction = "delete-cronjob"
    } else if (currentUrl == '/cockpit/kubernetes/job'){
      this.title = 'Job'
      this.createAction = "create-job";
      this.getAction= "get-job";
      this.updateAction = "update-job"
      this.deleteAction = "delete-job"
    } else if (currentUrl == '/cockpit/kubernetes/daemonset'){
      this.title = 'Daemonset'
      this.createAction = "create-daemonset";
      this.getAction= "get-daemonset";
      this.updateAction = "update-daemonset"
      this.deleteAction = "delete-daemonset"
    } else if (currentUrl == '/cockpit/kubernetes/configmap'){
      this.title = 'Configmap'
      this.createAction = "create-configmap";
      this.getAction= "get-configmap";
      this.updateAction = "update-configmap"
      this.deleteAction = "delete-configmap"
    } else if (currentUrl == '/cockpit/kubernetes/service'){
      this.title = 'Service'
      this.createAction = "create-service";
      this.getAction= "get-service";
      this.updateAction = "update-service"
      this.deleteAction = "delete-service"
    } else if (currentUrl == '/cockpit/kubernetes/ingress'){
      this.title = 'Ingress'
      this.createAction = "create-ingress";
      this.getAction= "get-ingress";
      this.updateAction = "update-ingress"
      this.deleteAction = "delete-ingress"
    }
    else if (currentUrl == '/cockpit/kubernetes/statefullset'){
      this.title = 'Statefullset'
      this.createAction = "create-statefulset";
      this.getAction= "get-statefulset";
      this.updateAction = "update-statefulset"
      this.deleteAction = "delete-statefulset"
    }
  }

  onActivate(component: any){
    component.check = true;
    this.action();
  }

}
export interface SendData {
  cul: string,
  na: string
}
