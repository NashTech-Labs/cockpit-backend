import {NgModule} from '@angular/core';

import {EmployeeFilterPipe} from './employee-filter/employee-filter.pipe';
import { SanitizeHtmlPipe } from './html-sanitizer/sanitize-html.pipe';
import {ReverseListPipe} from './reverse-list/reverse-list.pipe';
import {SplitCamelCasePipe} from './split-camel-case/split-camel-case.pipe';
import {SanitizeUrlPipe} from './url-sanitizer/sanitize-url.pipe';

@NgModule({
    exports: [ReverseListPipe, EmployeeFilterPipe, SplitCamelCasePipe, SanitizeHtmlPipe, SanitizeUrlPipe],
    declarations: [ReverseListPipe, EmployeeFilterPipe, SplitCamelCasePipe, SanitizeHtmlPipe, SanitizeUrlPipe],
})
export class CustomPipesModule {
}
