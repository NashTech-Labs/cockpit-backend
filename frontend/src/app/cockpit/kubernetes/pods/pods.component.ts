import {Component, OnDestroy, OnInit, TemplateRef} from '@angular/core';
import {CockpitService} from "../../cockpit.service";
import {SharedAddService} from "../../../shared-add.service";
import {Router} from "@angular/router";
import {Subscription} from "rxjs";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {type} from "os";


@Component({
  selector: 'app-pods',
  templateUrl: './pods.component.html',
  styleUrls: ['./pods.component.scss']
})
export class PodsComponent implements OnInit, OnDestroy{
  check: boolean = false;
  loading : boolean = false;
  tableRows: any;
  tableOffset: any;
  podsOverviewReqData: PodsReqData[];
  // @ts-ignore
  subscription: Subscription;
  // @ts-ignore
  private modalRef: BsModalRef;
  modalTitle: any;
  summary: boolean = false;
  events: boolean = false;
  logs: boolean = false;
  private isTarget: string;
  btnstyle: string;
  reqData: any;
  resData: any;
  logData: any;
  eventData: any;
  liveManifest: any
  deleteRequestData: any;
  activeRowData: any;

  constructor(private service: CockpitService,
              private router: Router,
              private sharedAddService: SharedAddService,
              private modalService: BsModalService,) {
  }

  ngOnInit() {
    this.subscription = this.sharedAddService.names$.subscribe(val=>{
      if (this.check) {
        this.podsOverviewReqData ={
          // @ts-ignore
          cluster_name: val.cul,
          action: "get-pod",
          user_name: "monkey_d_luffy",
          metadata:{
            namespace: val.na[0]?.namespace,
            all_namespaces: "False"
          }
        }
        this.getPodsOverviewData();
        this.loading = false;
        this.tableOffset = 0;
      }
    });
  }

  getPodsOverviewData() {
    this.service.namspaceList(this.podsOverviewReqData).subscribe((res) => {
      if(res){
        this.loading = true;
      }
      this.tableRows= res.data;
      console.log(res.data);
    });
  }

  isActiveRoute(routeUrl: string): boolean {
    return this.router.isActive(routeUrl, true);
  }

  onChange(event: any): void {
    this.tableOffset = event.offset;
  }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template, {
      animated: true,
      class:'right-modal',
    });
  }

  ngOnDestroy(): void {
    this.check = false;
  }

  onActiavte($event: any, addModal: TemplateRef<any>) {
    if($event.type == 'click'){
      if ($event.column && $event.column.name === 'NAME') {
        this.activeRowData= $event.row
        this.reqData = {
          // @ts-ignore
          cluster_name: this.podsOverviewReqData?.cluster_name,
          resource_name: $event.row.pod,
          namespace: $event.row.namespace,
          resource_kind: "Pod",
          user_name:'monkey_d_luffy'
        };
       this.service.k8sObjectSepcificDetails(this.reqData).subscribe(res=>{
         console.log(res);
         this.resData = res;
         this.logData = JSON.stringify(res.logs, undefined, 4);
         this.eventData = JSON.stringify(res.events, undefined, 4);
         this.liveManifest= JSON.stringify(res.live_manifest, undefined, 4);
         this.modalTitle = $event.row.pod
         this.openModal(addModal);
         this.summary = true;
         this.events = false;
         this.logs = false;
       });
      }
    }
  }

  openContent(data){
    if (data=='summary'){
      this.summary = true;
      this.events = false;
      this.logs = false;
    } else if (data=='events'){
      this.events = true;
      this.summary = false;
      this.logs = false;
    } else if (data=='logs'){
      this.logs = true;
      this.summary = false;
      this.events = false;

    }
  }

  cancelForm() {
    this.modalService.hide();
    this.summary = true;
    this.events = false;
    this.logs = false;
  }

  onDelete() {
    this.deleteRequestData = {
      // @ts-ignore
      cluster_name: this.podsOverviewReqData?.cluster_name,
      action: 'delete-pod',
      user_name: 'monkey_d_luffy',
      metadata: {
        namespace: this.activeRowData.namespace,
        k8s_object_name: this.activeRowData.pod,
      }
    };
    console.log(this.deleteRequestData);
    if (this.deleteRequestData !== '') {
      this.service.deleteKubernetes(this.deleteRequestData).subscribe(async (res) => {
        console.log(res);
      })
    }
  }
  
}

export interface PodsReqData {
  cluster_name: string,
  action: string,
  user_name: string,
  metadata:{
    namespace:string,
    all_namespaces: string
  }
}
