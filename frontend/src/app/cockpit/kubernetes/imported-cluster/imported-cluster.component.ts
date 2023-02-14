import { Component, Input, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {CockpitService} from "../../cockpit.service";


@Component({
  selector: 'app-imported-cluster',
  templateUrl: './imported-cluster.component.html',
  styleUrls: ['./imported-cluster.component.scss']
})
export class ImportedClusterComponent implements OnInit {

  // @ts-ignore
  @Input() tableRows: AuthorModel[];
  // @ts-ignore
  @Input() tableHeading: TableHeaderModel[];

  constructor(private service: CockpitService,
              private router: Router) { }

  ngOnInit(): void {
    this.service.getImportedCluster().subscribe((result)=>{
      console.log(result.clusters);
      this.tableRows = result.clusters;
    })
  }

  onActivate(event: any) {
    if (event.type === 'click') {
      if (event.column && event.column.name === 'CLUSTER NAME') {
        this.router.navigate(
          [`/dashboard`]
        );
      }
    }
  }
}
