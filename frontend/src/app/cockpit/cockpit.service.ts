import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {interval, Observable, Subject} from "rxjs";
import {mergeMap, takeUntil} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class CockpitService {
  sub: any;
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    }),
  };

  private myTemplates = `${environment.api.baseUrl}`;

  constructor(private httpClient: HttpClient) { }

  // @ts-ignore
  importCluster(data): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'import-cluster/',
      data
    );
  }

  // @ts-ignore
  createKubernetes(data): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'create-cluster-api/',
      data
    );
  }

  // @ts-ignore
  updateKubernetes(data): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'update-cluster-api/',
      data
    );
  }

  // @ts-ignore
  deleteKubernetes(data): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'delete-cluster-api/',
      data
    );
  }

  jenkinsRes(data: any): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'create-platform/',
      data
    );
  }

  getImportedCluster(): Observable<any>{
    return this.httpClient.get<any>(
      this.myTemplates + 'list-clusters/'
    );
  }

  namspaceList(data: any): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'get-cluster-api/',
      data
    );
  }

  clusterMonitoring(data: any): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'cluster-monitoring/',
      data
    );
  }

  k8sObjectSepcificDetails(data: any): Observable<any> {
    return this.httpClient.post<any>(
      this.myTemplates + 'get-k8s-object-sepcific-details/',
      data
    );
  }
    // clusterMonitoring(data: any): Pr
  //     this.myTemplates + 'cluster-monitoring/',
  //     data
  //   ).toPromise()
  //     .then(async res => {
  //       console.log(res);
  //       if (res.status_code == '4010') {
  //         return res;
  //       } else {
  //         setInterval(() => {
  //           this.clusterMonitoring(data)
  //         }, 30 * 1000);
  //         // setInterval(await this.clusterMonitoring(data), 30000)
  //       }
  //     })
  //     .catch(e=> console.log('error', e));
  // }
}
