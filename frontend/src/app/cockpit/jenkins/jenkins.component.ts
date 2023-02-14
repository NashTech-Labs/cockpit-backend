import {Component, OnInit, TemplateRef} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {SharedAddService} from "../../shared-add.service";
import {CockpitService} from "../cockpit.service";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {Router, RouterStateSnapshot} from "@angular/router";
import Swal from 'sweetalert2'
import * as  Guacamole from 'guacamole-common-js'
import {windowOpen} from "echarts/types/src/util/format";
import {element} from "protractor";
import {DomSanitizer} from "@angular/platform-browser";

@Component({
  selector: 'app-jenkins',
  templateUrl: './jenkins.component.html',
  styleUrls: ['./jenkins.component.scss']
})
export class JenkinsComponent implements OnInit {

  isFormValid: any;
  requestData: any;
  responseData: any;
  userName: string = 'Sachin155';
  userEmail: string = 'sachin.vd@knoldus.com';
  platform: string = 'jenkins';
  width:number;
  height:number;
  // subject: any;

  createForm: FormGroup = new FormGroup({
    git_url: new FormControl(''),
    git_branch: new FormControl(''),
    git_token: new FormControl(''),
    docker_reponame: new FormControl(''),
    docker_tag: new FormControl(''),
    docker_registry_url: new FormControl(''),
    docker_username: new FormControl(''),
    docker_password: new FormControl(''),
    docker_file_path: new FormControl(''),
    docker_build_context: new FormControl(''),
    language: new FormControl(''),
    version: new FormControl(''),
    framework: new FormControl('')

  });


  addForm: RequestData = {
    git_url: '',
    git_branch: '',
    git_token: '',
    docker_reponame: '',
    docker_tag: '',
    docker_registry_url: '',
    docker_username: '',
    docker_password: '',
    docker_file_path: '',
    docker_build_context: '',
    language: '',
    version: '',
    framework: '',
  };

  constructor(private sharedAddService: SharedAddService,
              private formBuilder: FormBuilder,
              private service: CockpitService,
              private modalService: BsModalService,
              private _router: Router,
              private modalRef: BsModalRef,
              private sanitizer: DomSanitizer) {
  }

  ngOnInit(): void {
    this.createDeployClusterForm();
    this.checkFormValidity();
    this.width= 900;
    this.height= 500;
  }

  onConnectInstance = () => {
    var display = document.getElementById("display");
    var tunnel = new Guacamole.Client(
      new Guacamole.WebSocketTunnel("ws://localhost:8081/guacamole/websocket-tunnel?token=D4A9D262B4FFE1D9599C91B758E72369CD72176744E063E56598BA81DC3C21B0&GUAC_DATA_SOURCE=postgresql&GUAC_ID=1&GUAC_TYPE=c&GUAC_WIDTH="+this.width+"&GUAC_HEIGHT="+this.height+"&GUAC_DPI=72&GUAC_TIMEZONE=Asia%2FCalcutta&GUAC_AUDIO=audio%2FL8&GUAC_AUDIO=audio%2FL16&GUAC_IMAGE=image%2Fjpeg&GUAC_IMAGE=image%2Fpng&GUAC_IMAGE=image%2Fwebp")
    );
    display.appendChild(tunnel.getDisplay().getElement());
    document.getElementsByTagName("canvas")[0].style.zIndex = '1'
    tunnel.connect();

    var mouse = new Guacamole.Mouse(tunnel.getDisplay().getElement());

    mouse.onmousedown =
      mouse.onmouseup =
        mouse.onmousemove = function (mouseState: any) {
          tunnel.sendMouseState(mouseState);
        };

    var keyboard = new Guacamole.Keyboard(document);

    keyboard.onkeydown = function (keysym: any) {
      tunnel.sendKeyEvent(1, keysym);
    };

    keyboard.onkeyup = function (keysym: any) {
      tunnel.sendKeyEvent(0, keysym);
    };
  }

  checkFormValidity() {
    this.createForm.statusChanges.pipe().subscribe(() => {
      this.isFormValid = this.createForm.valid;
    });
  }

  createDeployClusterForm() {
    this.createForm = this.formBuilder.group({
      git_url: [this.addForm.git_url, Validators.required ],
      git_branch: [this.addForm.git_branch, Validators.required],
      git_token: [this.addForm.git_token, Validators.required],
      docker_reponame: [this.addForm.docker_reponame, Validators.required],
      docker_tag: [this.addForm.docker_tag, Validators.required],
      docker_registry_url: [this.addForm.docker_registry_url],
      docker_username: [this.addForm.docker_username],
      docker_password: [this.addForm.docker_password],
      docker_file_path: [this.addForm.docker_file_path, Validators.required],
      docker_build_context: [this.addForm.docker_build_context],
      language: [this.addForm.language, Validators.required],
      version: [this.addForm.version, Validators.required],
      framework: [this.addForm.framework, Validators.required]
    });
  }

  async saveRequestData() {

    this.requestData = {
      // @ts-ignore
      user_name: this.userName,
      // @ts-ignore
      user_email: this.userEmail,
      // @ts-ignore
      platform: this.platform,
      // @ts-ignore
      project_details: {
        // @ts-ignore
        git_url: this.createForm.get('git_url').value,
        // @ts-ignore
        git_branch: this.createForm.get('git_branch').value,
        // @ts-ignore
        git_token: this.createForm.get('git_token').value,
        // @ts-ignore
        docker_reponame: this.createForm.get('docker_reponame').value,
        // @ts-ignore
        docker_tag: this.createForm.get('docker_tag').value,
        // @ts-ignore
        docker_registry_url: this.createForm.get('docker_registry_url').value,
        // @ts-ignore
        docker_username: this.createForm.get('docker_username').value,
        // @ts-ignore
        docker_password: this.createForm.get('docker_password').value,
        // @ts-ignore
        docker_file_path: this.createForm.get('docker_file_path').value,
        // @ts-ignore
        docker_build_context: this.createForm.get('docker_build_context').value,
        // @ts-ignore
        language: this.createForm.get('language').value,
        // @ts-ignore
        version: this.createForm.get('version').value,
        // @ts-ignore
        framework: this.createForm.get('framework').value,
      }
    };

    console.log(this.requestData);

    if (this.requestData != '') {
      await this.service.jenkinsRes(this.requestData).subscribe((res) => {
        // this.responseData = JSON.stringify(res, undefined, 4);
        this.responseData = res.message;
        Swal.fire(this.responseData);
      })
      this.createForm.reset();
    }

  }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template, {
      animated: true,
      class:'right-modal',
    });
  }

  cancelForm() {
    this.modalService.hide();
  }

}

export interface RequestData {
  git_url: string;
  git_branch: string;
  git_token: string;
  docker_reponame: string;
  docker_tag: string;
  docker_registry_url: string;
  docker_username: string;
  docker_password: string;
  docker_file_path: string;
  docker_build_context: string;
  language: string;
  version: string;
  framework: string;
}

