import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'reverse',
})
export class ReverseListPipe  implements PipeTransform {
  transform(list: any[]): any[] {
    return [...list].reverse();
  }
}
