import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'employeeFilter',
})
export class EmployeeFilterPipe implements PipeTransform {
    transform(employees: any[], parameter: string, searchTerm: string): any {
        if (!employees || !searchTerm) {
            return employees;
        }
        return employees.filter(employee => employee[parameter].toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1);
    }
}
