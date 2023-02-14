import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {CockpitComponent} from "./cockpit.component";
import {RouterModule, Routes} from "@angular/router";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {NgxDatatableModule} from "@swimlane/ngx-datatable";
import {ConfirmModalModule} from "../shared/confirm-modal/confirm-modal.module";
import {CustomPipesModule} from "../pipe/custom-pipes.module";
// import {AuthGuard} from "../auth/auth.guard";

export const routes: Routes = [
  {
    path: '',
    component: CockpitComponent,
    children: [
      {
        path: 'kubernetes',
        loadChildren: () =>
          import('./kubernetes/kubernetes.module').then((m) => m.KubernetesModule),
        // canActivate: [AuthGuard],
      },
      {
        path: 'jenkins',
        loadChildren: () =>
        import('./jenkins/jenkins.module').then((m) => m.JenkinsModule),
        // canActivate: [AuthGuard],
      },
    ],
    // canActivate: [AuthGuard],
  }
];


@NgModule({
  declarations: [
    CockpitComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule,
    NgxDatatableModule,
    ConfirmModalModule,
    CustomPipesModule,
  ]
})
export class CockpitModule { }
