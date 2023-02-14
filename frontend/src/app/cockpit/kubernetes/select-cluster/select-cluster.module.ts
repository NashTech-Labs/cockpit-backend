import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from "@angular/router";
import {PodsComponent} from "../pods/pods.component";
import {DeploymentsComponent} from "../deployments/deployments.component";
import {StatefullsetComponent} from "../statefullset/statefullset.component";
import {SecretComponent} from "../secret/secret.component";
import {DaemonsetComponent} from "../daemonset/daemonset.component";
import {CronjobComponent} from "../cronjob/cronjob.component";
import {JobComponent} from "../job/job.component";
import {ConfigmapComponent} from "../configmap/configmap.component";
import {SelectClusterComponent} from "./select-cluster.component";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {DeployKubernetesComponent} from "../deploy-kubernetes/deploy-kubernetes.component";
import {UpdateKubernetesComponent} from "../update-kubernetes/update-kubernetes.component";
import {DeleteKubernetesComponent} from "../delete-kubernetes/delete-kubernetes.component";
import {NgxDatatableModule} from "@swimlane/ngx-datatable";
import {ServicesComponent} from "../services/services.component";
import {IngressComponent} from "../ingress/ingress.component";
// import {AuthGuard} from "../../../auth/auth.guard";


export const routes: Routes = [
  {
    path: '',
    component: SelectClusterComponent,
    children: [
      {
        path: '',
        redirectTo: 'pods',
        pathMatch: 'full'
      },
      {
        path: 'pods',
        component: PodsComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'deployments',
        component: DeploymentsComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'statefullset',
        component: StatefullsetComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'secret',
        component: SecretComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'daemonset',
        component: DaemonsetComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'cronjob',
        component: CronjobComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'job',
        component: JobComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'configmap',
        component: ConfigmapComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'service',
        component: ServicesComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'ingress',
        component: IngressComponent,
        // canActivate: [AuthGuard],
      },
    ],
    // canActivate: [AuthGuard],
  }
];
@NgModule({
  declarations: [
    PodsComponent,
    DeploymentsComponent,
    StatefullsetComponent,
    SecretComponent,
    DaemonsetComponent,
    CronjobComponent,
    JobComponent,
    ConfigmapComponent,
    SelectClusterComponent,
    DeployKubernetesComponent,
    UpdateKubernetesComponent,
    DeleteKubernetesComponent,
    ServicesComponent,
    IngressComponent,
  ],
  imports: [
    ReactiveFormsModule,
    NgxDatatableModule,
    FormsModule,
    RouterModule.forChild(routes),
    CommonModule
  ]
})
export class SelectClusterModule { }
