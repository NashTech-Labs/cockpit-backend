import {Component, OnDestroy, OnInit, TemplateRef} from '@angular/core';
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {PodsReqData} from "../pods/pods.component";
import {Subscription} from "rxjs";
import {CockpitService} from "../../cockpit.service";
import {Router} from "@angular/router";
import {SharedAddService} from "../../../shared-add.service";

@Component({
  selector: 'app-configmap',
  templateUrl: './configmap.component.html',
  styleUrls: ['./configmap.component.scss']
})
export class ConfigmapComponent implements OnInit, OnDestroy {
  check: boolean = false;
  loading : boolean = false;
  tableRows: any;
  tableOffset: any;
  // @ts-ignore
  daemonsetOverviewReqData: PodsReqData[];
  // @ts-ignore
  subscription: Subscription;

  constructor(private service: CockpitService,
              private router: Router,
              private sharedAddService: SharedAddService,) { }

  ngOnInit(): void {
    this.subscription =  this.sharedAddService.names$.subscribe(val=>{
      if (this.check) {
        this.daemonsetOverviewReqData ={
          // @ts-ignore
          cluster_name: val.cul,
          action: "get-configmap",
          user_name: "monkey_d_luffy",
          metadata:{
            // @ts-ignore
            namespace:val.na[0]?.namespace,
            all_namespaces: "False"
          }
        }
        this.getDaemonsetOverviewData();
        this.loading = false;
        this.tableOffset = 0;
      }
    });
  }

  getDaemonsetOverviewData() {
    this.service.namspaceList(this.daemonsetOverviewReqData).subscribe((res) => {
      if(res){
        this.loading = true;
      }
      this.tableRows= res.data;
    });
  }

  onChange(event: any): void {
    this.tableOffset = event.offset;
  }

  ngOnDestroy(): void {
    this.check = false;
  }

}
