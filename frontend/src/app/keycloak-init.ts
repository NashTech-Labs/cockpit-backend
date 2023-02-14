// import { KeycloakService} from 'keycloak-angular';
//
// export function initializeKeycloak(keycloak: KeycloakService) {
//   return () =>
//     keycloak.init({
//       config: {
//         url: 'http://localhost:8080',
//         realm: 'Cockpit',
//         clientId: 'cockpit-ui'
//       },
//       initOptions: {
//         checkLoginIframe: true,
//         // onLoad: 'check-sso',
//         // silentCheckSsoRedirectUri:
//         //   window.location.origin + '/assets/silent-check-sso.html'
//       },
//       loadUserProfileAtStartUp: true,
//     });
// }

// export function initializeKeycloak(
//   keycloak: KeycloakService
// ) {
//
//   return () =>
//     keycloak.init({
//       config:{
//         url: 'http://localhost:8080/',
//         realm: 'Cockpit',
//         clientId: 'cockpit-ui'
//       },
//       // initOptions: {
//       //   onLoad: 'login-required',
//       //   flow: 'standard',
//       //   checkLoginIframe: true,
//       // },
//       // loadUserProfileAtStartUp: false,
//       // bearerExcludedUrls: []
//     });
// }
