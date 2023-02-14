import { Component, OnInit } from '@angular/core';
import {PodsReqData} from "../pods/pods.component";
import {Subscription} from "rxjs";
import {CockpitService} from "../../cockpit.service";
import {Router} from "@angular/router";
import {SharedAddService} from "../../../shared-add.service";

@Component({
  selector: 'app-ingress',
  templateUrl: './ingress.component.html',
  styleUrls: ['./ingress.component.scss']
})
export class IngressComponent implements OnInit {

  check: boolean = false
  loading : boolean = false;
  tableRows: any;
  tableOffset: any;
  // @ts-ignore
  deploymentOverviewReqData: PodsReqData[];
  // @ts-ignore
  subscription: Subscription;

  constructor(private service: CockpitService,
              private router: Router,
              private sharedAddService: SharedAddService,) {
  }

  ngOnInit(): void {
    this.subscription =  this.sharedAddService.names$.subscribe(val=>{
      if(this.check) {
        this.deploymentOverviewReqData ={
          // @ts-ignore
          cluster_name:  val.cul,
          action: "get-ingress",
          user_name: "monkey_d_luffy",
          metadata:{
            // @ts-ignore
            namespace:val.na[0]?.namespace,
            all_namespaces: "False"
          }
        }
        this.getDeploymentOverviewData();
        this.loading = false;
        this.tableOffset = 0;
      }
    })
  }

  getDeploymentOverviewData() {
    this.service.namspaceList(this.deploymentOverviewReqData).subscribe((res) => {
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
