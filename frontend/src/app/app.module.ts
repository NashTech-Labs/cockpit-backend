import {APP_INITIALIZER, NgModule} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {NgxDialogsModule} from "ngx-dialogs";
import { HttpClientModule} from "@angular/common/http";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {ToastrModule} from "ngx-toastr";
import {NgMultiSelectDropDownModule} from "ng-multiselect-dropdown";
// import {KeycloakAngularModule, KeycloakService} from "keycloak-angular";
// import {initializeKeycloak} from "./keycloak-init";


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxDialogsModule,
    HttpClientModule,
    // KeycloakAngularModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot({positionClass :'toast-top-right'}),
    NgMultiSelectDropDownModule.forRoot()
  ],
  providers: [
    // {
    //   // provide: APP_INITIALIZER,
    //   // useFactory: initializeKeycloak,
    //   // multi: true,
    //   // deps: [KeycloakService],
    // },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
