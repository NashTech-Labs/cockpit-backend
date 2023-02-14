import { Injectable } from '@angular/core';
import {BehaviorSubject, Observable, Subject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedAddService {
  private saveSubject = new Subject<any>();
  private editSubject = new Subject<any>();
  private editRadar = new Subject<boolean>();
  private submitRadar = new Subject<boolean>();
  private approveSubject = new Subject<boolean>();
  private rejectSubject = new Subject<boolean>();
  private approvedSubject = new Subject<string>();
  private rejectedSubject = new Subject<string>();
  private viewSubject = new Subject<any>();
  private resetSubject = new Subject<any>();
  private techSubject = new Subject<any>();

  sendSubmitClick(){
    this.saveSubject.next();
  }
  getSubmitClick():Observable<any>{
    return this.saveSubject.asObservable();
  }
  sendViewClick(){
    this.viewSubject.next();
  }
  getViewClick():Observable<any>{
    return this.viewSubject.asObservable();
  }

  private sub = new Subject();
  subj$ = this.sub.asObservable();

  send(value: string) {
    this.sub.next(value);
  }

  names$ = new BehaviorSubject<any>({cul: '', na: ''});

  sendName(value: string) {
    this.names$.next(value);
  }
}

