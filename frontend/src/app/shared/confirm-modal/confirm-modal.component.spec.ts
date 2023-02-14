import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BsModalRef, ModalModule } from 'ngx-bootstrap/modal';
import { ConfirmModalService } from '../confirm-modal.service';

import { ConfirmModalComponent } from './confirm-modal.component';

describe('ConfirmModalComponent', () => {
  let component: ConfirmModalComponent;
  let fixture: ComponentFixture<ConfirmModalComponent>;
  let service: ConfirmModalService;
  let bsModal: BsModalRef;
  const store = {};
  const mockLocalStorage = {
    getItem: (key: string): string => {
      return key in store ? store[key] : null;
    },
    setItem: (key: string, value: string) => {
      store[key] = `${value}`;
    },
    removeItem: (key: string) => {
      delete store[key];
    }
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ConfirmModalComponent],
      imports: [ModalModule.forRoot()],
      providers: [ConfirmModalService, BsModalRef]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfirmModalComponent);
    component = fixture.componentInstance;
    service = TestBed.inject(ConfirmModalService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should create', () => {
    component.ngOnInit();
    expect(component.onClose).toBeTruthy();
  });

  // it('should hide the component when confirmation msg is sent', () => {
  //   let remark= 'Okk Done!'
  //   spyOn(component.onClose, 'next').withArgs(true);
  //   component.confirm();
  //   localStorage.setItem('remark',JSON.stringify(remark));
  //   expect(component.onClose.next).toHaveBeenCalledWith(true);
  // });

  // it('should hide the component when confirmation decline is called', () => {
  //   spyOn(component.onClose, 'next').withArgs(false);
  //   component.decline();
  //   expect(component.onClose.next).toHaveBeenCalledWith(false);
  // });
});
