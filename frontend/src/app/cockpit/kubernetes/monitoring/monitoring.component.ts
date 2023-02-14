import {Component, OnInit} from '@angular/core';
import {CockpitService} from "../../cockpit.service";
import {Router} from "@angular/router";
import {SharedAddService} from "../../../shared-add.service";
import {ToastrService} from "ngx-toastr";
import {interval, Observable, of, Subject} from "rxjs";
import {catchError, map, mergeMap, takeUntil, takeWhile} from "rxjs/operators";
import { webSocket } from 'rxjs/webSocket';
import {HttpClient} from "@angular/common/http";
import {ClickType} from "@swimlane/ngx-datatable";
import {ajax} from "rxjs/ajax";
import {KeycloakService} from "keycloak-angular";

@Component({
  selector: 'app-monitoring',
  templateUrl: './monitoring.component.html',
  styleUrls: ['./monitoring.component.scss']
})
export class MonitoringComponent implements OnInit {

  clusters: any[] = [];
  tableOffset: any;
  reqData: any;
  selectedCluster: any;
  rows: any[]= [];
  tableRows: any;
  disabled: boolean = true;
  enable: boolean = false;
  prometheusStack:boolean= false;
  prometheusLink: any;
  res: any;
  loading : boolean = false;
  load: any[]= [];
  rowData: any;
  completeData: any;
  comDataArr: any[]= [];
  message: string ='';
  sub: any;
  mytimer: any;
  subject: any;
  userloggedIn: boolean = false;
  adminLoggedin: boolean = false;

  constructor(private service: CockpitService,
              private router: Router,
              private sharedAddService: SharedAddService,
              private toast: ToastrService,
              private httpClient: HttpClient,
              private keycloak: KeycloakService) {
  }

  ngOnInit(): void {
    this.userloggedIn = this.keycloak.isUserInRole('user');
    this.adminLoggedin = this.keycloak.isUserInRole('admin');
    console.log(this.userloggedIn);
    console.log(this.adminLoggedin);
    this.getClusterList();
    // this. subject= webSocket('ws://localhost:8849');
    // this.reqData = {
    //   cluster_name: 'basic-1',
    //   enable_monitoring: "true",
    //   namespace: "default"
    // }
  }

  getClusterList() {
    this.service.getImportedCluster().subscribe((res) => {
      for (let i = 0; i < res.clusters.length; i++) {
        this.loading= false;
        this.rowData = {
          cluster_name : res.clusters[i]?.cluster_name,
          enable_status: 'Click Here',
          stack_status: 'Not available',
          prometheus_url: '',
          apiserver_dashboard_status: 'Not available',
          container_dashboard_status: 'Not available',
          apiserver_dashboard_url: '',
          container_dashboard_url: ''
        }
        this.rows.push(this.rowData);
      }
      this.clusters = res.clusters;
    });
  }
  //
  // enableClick($event: any){
  //   this.subject.subscribe();
  //   this.subject.next(this.reqData);
  //   this.subject.complete();
  // }
  //
  // enableClick(rowIndex: any) {
  //   this.reqData = {
  //     cluster_name: this.rows[rowIndex]?.cluster_name,
  //     enable_monitoring: "true",
  //     namespace: "default"
  //   }
  //   const users = ajax({
  //     url: 'http://localhost:8000/cluster-monitoring/',
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'rxjs-custom-header': 'Rxjs'
  //     },
  //     body: {
  //       rxjs: this.reqData
  //     }
  //   }).pipe(
  //     map(response => console.log('response: ', response)),
  //     catchError(error => {
  //       console.log('error: ', error);
  //       return of(error);
  //     })
  //   );
  //   users.subscribe({
  //     next: value => console.log(value),
  //     error: err => console.log(err)
  //   });
  // }

  enableClick(rowIndex: any) {
    this.sub = new Subject();
    this.loading=  true;
    this.reqData = {
      cluster_name: this.rows[rowIndex]?.cluster_name,
      enable_monitoring: "true",
      namespace: "default"
    }
    interval(10000).pipe((takeUntil(this.sub)),
      mergeMap(  () => this.service.clusterMonitoring(this.reqData))
    )
      .subscribe((data: any) => {
        this.res = data
        if(this.res.status_code == "4000" || this.res.status_code == "4001" ||
          this.res.status_code == "4002" || this.res.status_code == "4004" ||
          this.res.status_code == "4005" || this.res.status_code == "4008") {
          this.toast.success(`${this.res.status_code}: ${this.res.message}`);
        }
        else if(this.res.status_code == "4003" || this.res.status_code == "4006" ||
          this.res.status_code == "4007") {
          this.toast.warning(`${this.res.status_code}: ${this.res.message}`);
          this.loading = false;
          this.rows[rowIndex] = {
            cluster_name : this.reqData.cluster_name,
            enable_status: 'Retry',
            stack_status: 'Deployment Failed',
            prometheus_url: '',
            apiserver_dashboard_status: 'Deployment Failed',
            container_dashboard_status: 'Deployment Failed',
            apiserver_dashboard_url: '',
            container_dashboard_url: ''
          };
          this.sub.next();
          this.sub.complete();
        }
        else if(this.res.status_code == "4009" || this.res.status_code == "4011") {
          this.toast.warning(`${this.res.status_code}: ${this.res.message}`);
          if(this.res.prometheus_server_url != 'None') {
            this.prometheusLink = this.res.prometheus_server_url;
            this.rows[rowIndex] = {
              cluster_name : this.reqData.cluster_name,
              enable_status: 'Retry',
              stack_status: 'Prometheus Url',
              prometheus_url: this.prometheusLink,
              apiserver_dashboard_status: 'Deployment Failed',
              container_dashboard_status: 'Deployment Failed',
              apiserver_dashboard_url: '',
              container_dashboard_url: ''
            }
            this.loading = false;
            this.sub.next();
            this.sub.complete();
          }
        }
        else if(this.res.status_code == "4010") {
          this.toast.success(`4010: ${this.res.message}`);
          if(this.res.prometheus_server_url != 'None') {
            this.prometheusLink = this.res.prometheus_server_url;
            this.rows[rowIndex] = {
              cluster_name : this.reqData.cluster_name,
              enable_status: 'Enabled',
              stack_status: 'Prometheus Url',
              prometheus_url: this.prometheusLink,
              apiserver_dashboard_status: 'Dashboard Url',
              container_dashboard_status: 'Dashboard Url',
              apiserver_dashboard_url: this.res.grafana_k8s_apiserver_dashboard_url,
              container_dashboard_url: this.res.grafana_k8s_container_dashboard_url
            }
            this.loading = false;
            this.sub.next();
            this.sub.complete();
          }
        }
      });
  }

  goToPrometheusStack(rowIndex: any) {
    window.open(this.rows[rowIndex]?.prometheus_url, "_blank");
  }
  goToApiServerDashboard(rowIndex: any) {
    window.open(this.rows[rowIndex]?.apiserver_dashboard_url, "_blank");
  }
  goToContainerDashboard(rowIndex: any) {
    window.open(this.rows[rowIndex]?.container_dashboard_url, "_blank");
  }

  reloadCurrentRoute() {
    let currentUrl = this.router.url;
    this.router.navigateByUrl('/', {skipLocationChange: true}).then(() => {
      this.router.navigate([currentUrl]);
    });
  }

}

// getClusterList() {
//   this.service.getImportedCluster().subscribe((res) => {
//     this.tableRows = res.clusters;
//     this.clusters = res.clusters;
//   });
// }


//@ts-ignore
// selectCluster(event) {
//   // @ts-ignore
//   this.selectedCluster = this.clusters?.filter((cluster)=> cluster.cluster_name === event.target.value);
//   this.rowData = {
//     cluster_name : this.selectedCluster[0]?.cluster_name,
//     stack_status: '',
//     prometheus_url: '',
//     apiserver_dashboard_status: '',
//     container_dashboard_status: '',
//     apiserver_dashboard_url: '',
//     container_dashboard_url: ''
//   }
//   this.reqData = {
//     cluster_name: this.selectedCluster[0]?.cluster_name,
//     enable_monitoring:  "true",
//     namespace: "default"
//   }
//   this.disabled = false;
// }

// enableClick() {
//   this.sub = new Subject();
//   this.rows.push(this.rowData);
//   this.completeData = {
//     cluster_name : '',
//     prometheus_url: ''
//   };
//    this.load.push({
//      loading: true,
//    });
//   interval(10000).pipe((takeUntil(this.sub)),
//      mergeMap(  () => this.service.clusterMonitoring(this.reqData))
//    )
//      .subscribe((data: any) => {
//        this.res = data
//        if(this.res.status_code == "4000") {
//          this.toast.success(`4000: ${this.res.message}`);
//        }
//        else if(this.res.status_code == "4001") {
//          this.toast.success(`4001: ${this.res.message}`);
//        }
//        else if(this.res.status_code == "4002") {
//          this.toast.success(`4002: ${this.res.message}`);
//        }
//        else if(this.res.status_code == "4003") {
//          this.toast.warning(`4003: ${this.res.message}`);
//          this.load[this.load.length -1].loading = false;
//          this.rows[this.load.length -1] = {
//            cluster_name : this.reqData.cluster_name,
//            stack_status: 'Deployment Failed',
//            prometheus_url: '',
//            apiserver_dashboard_status: 'Deployment Failed',
//            container_dashboard_status: 'Deployment Failed',
//            apiserver_dashboard_url: '',
//            container_dashboard_url: ''
//          };
//          this.sub.next();
//          this.sub.complete();
//        }
//        else if(this.res.status_code == "4004") {
//          this.toast.success(`4004: ${this.res.message}`);
//        }
//        else if(this.res.status_code == "4005") {
//          this.toast.success(`4005: ${this.res.message}`);
//        }
//        else if(this.res.status_code == "4006") {
//          this.toast.warning(`4006: ${this.res.message}`);
//          this.load[this.load.length -1].loading = false;
//          this.rows[this.load.length -1] = {
//            cluster_name : this.reqData.cluster_name,
//            stack_status: 'Deployment Failed',
//            prometheus_url: '',
//            apiserver_dashboard_status: 'Deployment Failed',
//            container_dashboard_status: 'Deployment Failed',
//            apiserver_dashboard_url: '',
//            container_dashboard_url: ''
//          };
//          this.sub.next();
//          this.sub.complete();
//        }
//        else if(this.res.status_code == "4007") {
//          this.toast.warning(`4007: ${this.res.message}`);
//          this.load[this.load.length -1].loading = false;
//          this.rows[this.load.length -1] = {
//            cluster_name : this.reqData.cluster_name,
//            stack_status: 'Deployment Failed',
//            prometheus_url: '',
//            apiserver_dashboard_status: 'Deployment Failed',
//            container_dashboard_status: 'Deployment Failed',
//            apiserver_dashboard_url: '',
//            container_dashboard_url: ''
//          };
//          this.sub.next();
//          this.sub.complete();
//        }
//        else if(this.res.status_code == "4008") {
//          this.toast.success(`4008: ${this.res.message}`);
//        }
//        else if(this.res.status_code == "4009") {
//          this.toast.warning(`4009: ${this.res.message}`);
//          if(this.res.prometheus_server_url != 'None') {
//            this.prometheusLink = this.res.prometheus_server_url;
//            this.rows[this.load.length -1] = {
//              cluster_name : this.reqData.cluster_name,
//              stack_status: 'Prometheus Url',
//              prometheus_url: this.prometheusLink,
//              apiserver_dashboard_status: 'Deployment Failed',
//              container_dashboard_status: 'Deployment Failed',
//              apiserver_dashboard_url: '',
//              container_dashboard_url: ''
//            }
//            this.load[this.load.length -1].loading = false;
//            this.sub.next();
//            this.sub.complete();
//          }
//        }
//        else if(this.res.status_code == "4010") {
//          this.toast.success(`4010: ${this.res.message}`);
//          if(this.res.prometheus_server_url != 'None') {
//            this.prometheusLink = this.res.prometheus_server_url;
//            this.rows[this.load.length -1] = {
//              cluster_name : this.reqData.cluster_name,
//              stack_status: 'Prometheus Url',
//              prometheus_url: this.prometheusLink,
//              apiserver_dashboard_status: 'Dashboard Url',
//              container_dashboard_status: 'Dashboard Url',
//              apiserver_dashboard_url: this.res.grafana_k8s_apiserver_dashboard_url,
//              container_dashboard_url: this.res.grafana_k8s_container_dashboard_url
//            }
//            this.load[this.load.length -1].loading = false;
//            this.sub.next();
//            this.sub.complete();
//          }
//        }
//        else if(this.res.status_code == "4011") {
//          this.toast.success(`4011: ${this.res.message}`);
//          if(this.res.prometheus_server_url != 'None') {
//            this.prometheusLink = this.res.prometheus_server_url;
//            this.rows[this.load.length -1] = {
//              cluster_name : this.reqData.cluster_name,
//              stack_status: 'Prometheus Url',
//              prometheus_url: this.prometheusLink,
//              apiserver_dashboard_status: 'Deployment Failed',
//              container_dashboard_status: 'Deployment Failed',
//              apiserver_dashboard_url: '',
//              container_dashboard_url: ''
//            }
//            this.load[this.load.length -1].loading = false;
//            this.sub.next();
//            this.sub.complete();
//          }
//        }
//      });
//  }


// enableMonitoring(rowIndex: any) {
//   this.loading = true;
//   this.reqData = {
//     cluster_name: this.rows[rowIndex]?.cluster_name,
//     enable_monitoring: "true",
//     namespace: "default"
//   }
//   return new Promise<any>((resolve, reject) => {
//     this.httpClient.post<any>(
//       'http://localhost:8000/cluster-monitoring/',
//       this.reqData
//     ).toPromise().then(res => {
//       if (res.status_code == '4000') {
//         this.mytimer = setInterval(() => {
//           this.serviceCall(this.reqData).then(res => {
//             if(res.status_code == "4001" || res.status_code == "4002" || res.status_code == "4004" ||
//               res.status_code == "4005" || res.status_code == "4008") {
//               this.toast.success(`${res.status_code}: ${res.message}`);
//             }
//             else if (res.status_code == "4010") {
//               this.toast.success(`4010: ${res.message}`);
//               if (res.prometheus_server_url != 'None') {
//                 this.prometheusLink = res.prometheus_server_url;
//                 this.rows[rowIndex] = {
//                   cluster_name: this.reqData.cluster_name,
//                   enable_status: 'Enabled',
//                   stack_status: 'Prometheus Url',
//                   prometheus_url: this.prometheusLink,
//                   apiserver_dashboard_status: 'Dashboard Url',
//                   container_dashboard_status: 'Dashboard Url',
//                   apiserver_dashboard_url: res.grafana_k8s_apiserver_dashboard_url,
//                   container_dashboard_url: res.grafana_k8s_container_dashboard_url
//                 }
//                 this.loading = false;
//                 clearInterval(this.mytimer);
//               }
//             }
//             else if (res.status_code == "4003" || res.status_code == "4006" ||
//               res.status_code == "4007") {
//               this.toast.warning(`${res.status_code}: ${res.message}`);
//               this.loading = false;
//               this.rows[rowIndex] = {
//                 cluster_name: this.reqData.cluster_name,
//                 enable_status: 'Retry',
//                 stack_status: 'Deployment Failed',
//                 prometheus_url: '',
//                 apiserver_dashboard_status: 'Deployment Failed',
//                 container_dashboard_status: 'Deployment Failed',
//                 apiserver_dashboard_url: '',
//                 container_dashboard_url: ''
//               };
//               clearInterval(this.mytimer);
//             }
//             else if (res.status_code == "4009" || res.status_code == "4011") {
//               this.toast.warning(`${res.status_code}: ${res.message}`);
//               if (res.prometheus_server_url != 'None') {
//                 this.prometheusLink = res.prometheus_server_url;
//                 this.rows[rowIndex] = {
//                   cluster_name: this.reqData.cluster_name,
//                   enable_status: 'Retry',
//                   stack_status: 'Prometheus Url',
//                   prometheus_url: this.prometheusLink,
//                   apiserver_dashboard_status: 'Deployment Failed',
//                   container_dashboard_status: 'Deployment Failed',
//                   apiserver_dashboard_url: '',
//                   container_dashboard_url: ''
//                 }
//                 this.loading = false;
//                 clearInterval(this.mytimer);
//               }
//             }
//           }).catch(e => console.log('error', e));
//         }, 10 * 1000);
//       }
//       else if (res.status_code == "4010") {
//         this.toast.success(`4010: ${res.message}`);
//         if (res.prometheus_server_url != 'None') {
//           this.prometheusLink = res.prometheus_server_url;
//           this.rows[rowIndex] = {
//             cluster_name: this.reqData.cluster_name,
//             enable_status: 'Enabled',
//             stack_status: 'Prometheus Url',
//             prometheus_url: this.prometheusLink,
//             apiserver_dashboard_status: 'Dashboard Url',
//             container_dashboard_status: 'Dashboard Url',
//             apiserver_dashboard_url: res.grafana_k8s_apiserver_dashboard_url,
//             container_dashboard_url: res.grafana_k8s_container_dashboard_url
//           }
//           this.loading = false;
//         }
//       } else if (res.status_code == "4003" || res.status_code == "4006" ||
//         res.status_code == "4007") {
//         this.toast.warning(`${res.status_code}: ${res.message}`);
//         this.loading = false;
//         this.rows[rowIndex] = {
//           cluster_name: this.reqData.cluster_name,
//           enable_status: 'Retry',
//           stack_status: 'Deployment Failed',
//           prometheus_url: '',
//           apiserver_dashboard_status: 'Deployment Failed',
//           container_dashboard_status: 'Deployment Failed',
//           apiserver_dashboard_url: '',
//           container_dashboard_url: ''
//         };
//       } else if (res.status_code == "4009" || res.status_code == "4011") {
//         this.toast.warning(`${res.status_code}: ${res.message}`);
//         if (res.prometheus_server_url != 'None') {
//           this.prometheusLink = res.prometheus_server_url;
//           this.rows[rowIndex] = {
//             cluster_name: this.reqData.cluster_name,
//             enable_status: 'Retry',
//             stack_status: 'Prometheus Url',
//             prometheus_url: this.prometheusLink,
//             apiserver_dashboard_status: 'Deployment Failed',
//             container_dashboard_status: 'Deployment Failed',
//             apiserver_dashboard_url: '',
//             container_dashboard_url: ''
//           }
//           this.loading = false;
//         }
//       } }
//     ).catch(e1 => {
//       return console.log('error', e1);
//     })
//   })
// }

// serviceCall(req: any) {
//   console.log('checkintervalcount')
//   return this.httpClient.post<any>(
//     'http://localhost:8000/cluster-monitoring/',
//     req
//   ).toPromise().then(res=> {
//       return res;
//   }).catch(e=> console.log('error', e));
// }
