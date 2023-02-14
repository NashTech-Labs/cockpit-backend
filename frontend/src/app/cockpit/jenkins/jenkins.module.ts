import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from "@angular/router";
import {JenkinsComponent} from "./jenkins.component";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {AlertModule} from "ngx-bootstrap/alert";
// import {AuthGuard} from "../../auth/auth.guard";

export const routes: Routes = [
  {

    path: '',
    component: JenkinsComponent,
    children: [
      {
        path: 'jenkins',
        component: JenkinsComponent,
        // canActivate: [AuthGuard],
      },
    ],
    // canActivate: [AuthGuard],
  }
]

@NgModule({
  declarations: [JenkinsComponent],
  imports: [
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    RouterModule.forChild(routes),
    AlertModule,
  ]
})
export class JenkinsModule { }
