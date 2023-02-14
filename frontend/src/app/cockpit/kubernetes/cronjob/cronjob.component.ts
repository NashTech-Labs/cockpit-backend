import {Component, OnDestroy, OnInit, TemplateRef} from '@angular/core';
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {PodsReqData} from "../pods/pods.component";
import {CockpitService} from "../../cockpit.service";
import {Router} from "@angular/router";
import {SharedAddService} from "../../../shared-add.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-cronjob',
  templateUrl: './cronjob.component.html',
  styleUrls: ['./cronjob.component.scss']
})
export class CronjobComponent implements OnInit, OnDestroy{
  loading: boolean =false;
  check: boolean = false;
  tableRows: any;
  tableOffset: any;
  // @ts-ignore
  daemonsetOverviewReqData: PodsReqData[];
  // @ts-ignore
  subscription: Subscription;

  constructor(private service: CockpitService,
              private router: Router,
              private modalService: BsModalService,
              private sharedAddService: SharedAddService,) { }

  ngOnInit(): void {
    this.subscription =  this.sharedAddService.names$.subscribe(val=>{
      if (this.check) {
        this.daemonsetOverviewReqData ={
          // @ts-ignore
          cluster_name:  val.cul,
          action: "get-cronjob",
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
    })
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
