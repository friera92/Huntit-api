import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { Catalog, Species } from '../services/regulations.service';
import { Home } from './home';
import { AuthService } from '../services/auth.service';

const species: Species[] = [{ id: 7, name: 'Wild Hog', scientific: 'Sus scrofa', image: '/hog.png', about: '', behavior: '', tactics: '' }];
const catalog: Catalog = {
  land_types: [
    { id: 2, name: 'Private Land', is_private: true, requires_managed_area: false },
    { id: 3, name: 'Public WMA', is_private: false, requires_managed_area: true }
  ],
  zones: [{ id: 4, code: 'A', name: 'Zone A' }],
  dmus: [{ id: 5, code: 'A1', zone_id: 4 }],
  regulatory_areas: [],
  managed_areas: [{ id: 6, name: 'Example WMA', area_type: 'WMA' }]
};

describe('Home API search integration', () => {
  let component: Home;
  let fixture: ComponentFixture<Home>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Home],
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(Home);
    component = fixture.componentInstance;
    fixture.detectChanges();
    http.expectOne('/api/auth/me/').flush({ detail: 'Not authenticated.' }, { status: 401, statusText: 'Unauthorized' });
  });

  afterEach(() => http.verify());

  function load(): void {
    http.expectOne('/api/species/').flush(species);
    http.expectOne('/api/catalog/').flush(catalog);
    fixture.detectChanges();
  }

  it('loads live species and sends IDs, geography and the selected date in the URL', () => {
    load();
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    component.selectSpecies(species[0]);
    component.huntingDate = '2026-11-03';
    component.zone = '4';
    component.dmu = '5';
    component.landownerPermission = true;
    component.checkRegulations();
    expect(navigate).toHaveBeenCalledWith(['/results'], {
      queryParams: {
        species: '7', land_type: '2', date: '2026-11-03', zone: '4', dmu: '5',
        regulatory_area: '', managed_area: '', landowner_permission: 'true'
      }
    });
    expect(component.speciesList()).toEqual(species);
  });

  it('requires a specific managed area for public land', () => {
    load();
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    component.selectSpecies(species[0]);
    component.setLandType(3);
    component.checkRegulations();
    expect(navigate).not.toHaveBeenCalled();
    expect(component.error()).toContain('Select a public managed area');
    component.managedArea = '6';
    component.checkRegulations();
    expect(navigate).toHaveBeenCalled();
  });

  it('shows connection errors instead of using hardcoded species', () => {
    http.expectOne('/api/catalog/').flush(catalog);
    http.expectOne('/api/species/').flush('Unavailable', { status: 503, statusText: 'Unavailable' });
    fixture.detectChanges();
    expect(component.speciesList()).toEqual([]);
    expect(component.loading()).toBe(false);
    expect(fixture.nativeElement.textContent).toContain('Unable to load species');
  });

  it('fills a new search from saved preferences without storing a guest history', () => {
    load();
    TestBed.inject(AuthService).login({ username: 'qa', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/login/').flush({ id: 1, username: 'qa', email: '', first_name: '', last_name: '', is_staff: false });
    fixture.detectChanges();
    http.expectOne('/api/personal/preferences/').flush({ species: [7], managed_areas: [6], zones: [4] });
    expect(component.selectedSpecies?.id).toBe(7); expect(component.zone).toBe('4');
    expect(component.landType).toBe('3'); expect(component.managedArea).toBe('6');
    expect(component.landownerPermission).toBe(false);
  });

  it('clears account-derived defaults on logout while the Home component stays mounted', () => {
    load();
    const auth = TestBed.inject(AuthService);
    auth.login({ username: 'qa', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/login/').flush({ id: 1, username: 'qa' });
    fixture.detectChanges();
    http.expectOne('/api/personal/preferences/').flush({ species: [7], managed_areas: [6], zones: [4] });
    auth.logout().subscribe(); http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/logout/').flush(null, { status: 204, statusText: 'No Content' });
    fixture.detectChanges();
    expect(component.selectedSpecies).toBeNull(); expect(component.zone).toBe(''); expect(component.managedArea).toBe('');
    expect(component.landType).toBe('2'); expect(component.preferenceNotice()).toBe('');
  });

  it('cancels a preference request after logout without blocking the public catalog', () => {
    load();
    const auth = TestBed.inject(AuthService);
    auth.login({ username: 'qa', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({}); http.expectOne('/api/auth/login/').flush({ id: 1, username: 'qa' });
    fixture.detectChanges();
    const preferences = http.expectOne('/api/personal/preferences/');
    auth.logout().subscribe(); http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/logout/').flush(null, { status: 204, statusText: 'No Content' });
    fixture.detectChanges();
    expect(preferences.cancelled).toBe(true); expect(component.loading()).toBe(false);
    expect(component.speciesList()).toEqual(species); expect(component.selectedSpecies).toBeNull();
  });

  it('names covered managed areas and identifies unsupported selections', () => {
    load(); component.selectedSpecies = species[0]; component.landType = '3'; component.managedArea = '6';
    const scope = { title: 'Hog WMA coverage', species: 7, land_type: 3, scopes: { managed_area: [6] }, coverage: { start_date: '2026-01-01', end_date: '2026-12-31' }, reviewed: false };
    component.catalog.set({ ...catalog, supported_scopes: [scope] });
    expect(component.scopeAreaNames(scope)).toBe('Example WMA'); expect(component.unsupportedManagedArea).toBe(false);
    component.managedArea = '99'; expect(component.unsupportedManagedArea).toBe(true);
  });
});
