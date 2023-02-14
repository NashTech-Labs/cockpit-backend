import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {KeycloakService} from "keycloak-angular";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  // // @ts-ignore
  // navItems: NavBarItemModel[];
  // // @ts-ignore
  // childrens: any[];
  // // @ts-ignore
  // xyz: any;
  // status: boolean = false;
  // isMobile: boolean = false;
  // toggleSideNav: boolean = false;
  // dropdownClick: boolean = false;
  // constructor(private router: Router,
  // private keycloak: KeycloakService) { }
  //
  // async ngOnInit() {
  //   if (window.innerWidth < 768) {
  //     this.isMobile = true;
  //     console.log(window.innerWidth);
  //   }
  //
  //   this.navItems = [
  //     {
  //       title: 'Cockpit',
  //       link: '',
  //       imageUrl: '',
  //       isNavbarLevelItem: true,
  //       minRole: 1,
  //       collapsed: true,
  //       childerens: [
  //         {
  //           title: 'Kubernetes',
  //           link: '',
  //           imageUrl: '',
  //           isNavbarLevelItem: false,
  //           minRole: 1,
  //           collapsed: true,
  //           childerens: [
  //             {
  //               title: 'Cluster',
  //               link: '/cockpit/kubernetes/cluster',
  //               imageUrl: 'attractions',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Pods',
  //               link: '/cockpit/kubernetes/pods',
  //               imageUrl: 'control_camera',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Deployments',
  //               link: '/cockpit/kubernetes/deployments',
  //               imageUrl: 'hub',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Statefullset',
  //               link: '/cockpit/kubernetes/statefullset',
  //               imageUrl: 'join_full',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Secrets',
  //               link: '/cockpit/kubernetes/secret',
  //               imageUrl: 'vpn_key',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Namespaces',
  //               link: '/cockpit/kubernetes/namespaces',
  //               imageUrl: 'list_alt',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Cronjobs',
  //               link: '/cockpit/kubernetes/cronjob',
  //               imageUrl: 'content_copy',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Jobs',
  //               link: '/cockpit/kubernetes/job',
  //               imageUrl: 'work',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Daemonsets',
  //               link: '/cockpit/kubernetes/daemonset',
  //               imageUrl: 'list',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Configmap',
  //               link: '/cockpit/kubernetes/configmap',
  //               imageUrl: 'center_focus_weak',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Services',
  //               link: '/cockpit/kubernetes/service',
  //               imageUrl: 'lan',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Ingress',
  //               link: '/cockpit/kubernetes/ingress',
  //               imageUrl: 'lan',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //             {
  //               title: 'Monitoring',
  //               link: '/cockpit/kubernetes/monitoring',
  //               imageUrl: 'legend_toggle',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //           ]
  //         },            {
  //           title: 'Jenkins',
  //           link: '/cockpit/jenkins',
  //           imageUrl: 'article',
  //           isNavbarLevelItem: false,
  //           minRole: 1,
  //           childerens: [
  //             {
  //               title: 'Jenkins',
  //               link: '/cockpit/jenkins',
  //               imageUrl: 'legend_toggle',
  //               isNavbarLevelItem: false,
  //               minRole: 1,
  //             },
  //           ]
  //         },
  //       ]
  //     },
  //   ];
  //
  //   // @ts-ignore
  //   this.childrens = this.navItems[0].childerens;
  //
  // }
  //
  // isActiveRoute(routeUrl: string): boolean {
  //   return this.router.isActive(routeUrl, true);
  // }
  // toggleSideBar() {
  //   this.toggleSideNav = !this.toggleSideNav;
  // }
  //  logoutCockpit() {
  //   // localStorage.clear();
  //   // this.keycloak.clearToken();
  //   this.keycloak.logout().then(res=> console.log(res)).catch(e=> console.log(e))
  // }
}

export interface NavBarItemModel {
  title: string;
  link: string;
  imageUrl: string;
  isNavbarLevelItem: boolean;
  minRole?: number;
  collapsed?: boolean;
  childerens?: NavBarItemModel[];
}
