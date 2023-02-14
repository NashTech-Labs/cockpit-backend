import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'splitCamelCase',
})
export class SplitCamelCasePipe implements PipeTransform {
  transform(inputString: string): string {
    return inputString.split(/(?=[A-Z])/).join(' ');
  }
}
