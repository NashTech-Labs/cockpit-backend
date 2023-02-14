import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClusterComponent } from './cluster/cluster.component';
import { PodsComponent } from './pods/pods.component';
import {RouterModule, Routes} from "@angular/router";
import {KubernetesComponent} from "./kubernetes.component";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { ExistingClusterComponent } from './existing-cluster/existing-cluster.component';
import { ImportedClusterComponent } from './imported-cluster/imported-cluster.component';
import {NgxDatatableModule} from "@swimlane/ngx-datatable";
import {ConfirmModalModule} from "../../shared/confirm-modal/confirm-modal.module";
import {CustomPipesModule} from "../../pipe/custom-pipes.module";
import {NgMultiSelectDropDownModule} from "ng-multiselect-dropdown";
import {AlertModule} from "ngx-bootstrap/alert";
import {NamespacesComponent} from "./namespaces/namespaces.component";
import { MonitoringComponent } from './monitoring/monitoring.component';
// import {AuthGuard} from "../../auth/auth.guard";


export const routes: Routes = [
  {
    path: '',
    component: KubernetesComponent,
    children: [
      {
        path: '',
        redirectTo: 'cluster',
        pathMatch: 'full'
      },
      {
        path: 'cluster',
        component: ClusterComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'namespaces',
        component: NamespacesComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: 'monitoring',
        component: MonitoringComponent,
        // canActivate: [AuthGuard],
      },
      {
        path: '',
        loadChildren: () =>
          import('./select-cluster/select-cluster.module').then((m) => m.SelectClusterModule),
        // canActivate: [AuthGuard],
      },
    ],
    // canActivate: [AuthGuard],
  }
];


@NgModule({
  declarations: [
    KubernetesComponent,
    ClusterComponent,
    NamespacesComponent,
    ExistingClusterComponent,
    ImportedClusterComponent,
    MonitoringComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule,
    NgxDatatableModule,
    ConfirmModalModule,
    CustomPipesModule,
    NgMultiSelectDropDownModule,
    AlertModule,
  ]
})
export class KubernetesModule { }
