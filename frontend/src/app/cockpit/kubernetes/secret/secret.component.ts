import {Component, OnDestroy, OnInit} from '@angular/core';
import {PodsReqData} from "../pods/pods.component";
import {CockpitService} from "../../cockpit.service";
import {Router} from "@angular/router";
import {SharedAddService} from "../../../shared-add.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-secret',
  templateUrl: './secret.component.html',
  styleUrls: ['./secret.component.scss']
})
export class SecretComponent implements OnInit, OnDestroy{
  check: boolean = false;
  loading : boolean = false;
  tableRows: any;
  tableOffset: any;
  // @ts-ignore
  secretOverviewReqData: PodsReqData[];
  // @ts-ignore
  subscription: Subscription;

  constructor(private service: CockpitService,
              private router: Router,
              private sharedAddService: SharedAddService,) { }

  ngOnInit(): void {
    this.subscription =  this.sharedAddService.names$.subscribe(val=>{
      if(this.check) {
        this.secretOverviewReqData ={
          // @ts-ignore
          cluster_name:  val.cul,
          action: "get-secret",
          user_name: "monkey_d_luffy",
          metadata:{
            // @ts-ignore
            namespace:val.na[0]?.namespace,
            all_namespaces: "False"
          }
        }
        this.getSecretOverviewData();
        this.loading = false;
        this.tableOffset = 0;
      }
    })
  }

  getSecretOverviewData() {
    this.service.namspaceList(this.secretOverviewReqData).subscribe((res) => {
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
