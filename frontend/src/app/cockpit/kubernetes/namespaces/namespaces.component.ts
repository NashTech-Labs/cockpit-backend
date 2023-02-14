import { Component, OnInit } from '@angular/core';
import {Subscription} from "rxjs";
import {CockpitService} from "../../cockpit.service";
import {Router} from "@angular/router";
import {SharedAddService} from "../../../shared-add.service";
import {PodsReqData} from "../pods/pods.component";

@Component({
  selector: 'app-namespaces',
  templateUrl: './namespaces.component.html',
  styleUrls: ['./namespaces.component.scss']
})
export class NamespacesComponent implements OnInit {
  clusters: any[] = [];
  tableOffset: any;
  namespaceReqData: any;
  selectedCluster: any;
  namespaces: any= [];
  namespaceRes: any;
  tableRows: any;

  constructor(private service: CockpitService,
              private router: Router,
              private sharedAddService: SharedAddService,) {
  }

  ngOnInit(): void {
    this.getClusterList();
  }

  getClusterList() {
    this.service.getImportedCluster().subscribe((res) => {
      this.clusters = res.clusters;
    });
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
        namespace:"",
        all_namespaces: "True"
      }
    }
    this.getNamespaceList();
    this.tableOffset = 0;
  }

  getNamespaceList() {
    this.service.namspaceList(this.namespaceReqData).subscribe((res) => {
      this.namespaceRes = res;
      this.tableRows = res.data;
    });
  }

  onChange(event: any): void {
    this.tableOffset = event.offset;
  }

  reloadCurrentRoute() {
    let currentUrl = this.router.url;
    this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
      this.router.navigate([currentUrl]);
    });
  }
}
