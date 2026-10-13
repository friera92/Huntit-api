import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UserLicense } from '../services/personal.service';
import { Licenses } from './licenses';

const license: UserLicense = { id: 4, permit: null, name: 'Hunting license', status: 'held', valid_from: '2026-01-01', expires_on: '2026-12-31', notes: '' };

describe('License account wallet', () => {
  let fixture: ComponentFixture<Licenses>;
  let http: HttpTestingController;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Licenses], providers: [provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(Licenses);
    fixture.detectChanges();
    http.expectOne('/api/personal/licenses/').flush([]);
    http.expectOne('/api/catalog/').flush({ land_types: [], zones: [], dmus: [], managed_areas: [], regulatory_areas: [], license_permits: [{ id: 2, name: 'Hunting license' }] });
    fixture.detectChanges();
    await fixture.whenStable();
  });
  afterEach(() => http.verify());

  it('starts empty with no fake license numbers and clearly states self-reported status', () => {
    expect(fixture.nativeElement.textContent).toContain('No license statuses saved yet');
    expect(fixture.nativeElement.textContent).toContain('self-reported');
    expect(fixture.nativeElement.textContent).not.toContain('FWC-12345678');
  });

  it('creates and edits a persistent license using its server ID', () => {
    const component = fixture.componentInstance;
    const { id, ...form } = license;
    component.form = form;
    component.saveLicense();
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/personal/licenses/').flush(license);
    expect(component.myLicenses()).toEqual([license]);
    component.editLicense(license);
    component.form.status = 'expired';
    component.saveLicense();
    http.expectOne('/api/auth/csrf/').flush({});
    const update = http.expectOne('/api/personal/licenses/4/');
    expect(update.request.method).toBe('PATCH');
    expect(update.request.body.status).toBe('expired');
    update.flush({ ...license, status: 'expired' });
    expect(component.myLicenses()[0].status).toBe('expired');
    expect(component.editingId).toBeUndefined();
  });

  it('retains a record when deletion fails offline', () => {
    const component = fixture.componentInstance;
    component.myLicenses.set([license]);
    component.deleteLicense(license);
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/personal/licenses/4/').error(new ProgressEvent('error'));
    expect(component.myLicenses()).toEqual([license]);
    expect(component.error()).toContain('Cannot reach');
    expect(component.busy()).toBe(false);
  });
});
