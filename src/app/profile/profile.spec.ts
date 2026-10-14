import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { SavedSearch } from '../services/personal.service';
import { Profile } from './profile';

const search: SavedSearch = { id: 5, title: 'Weekend hog', species: 1, land_type: 1, hunting_date: '2026-11-03', zone: null, dmu: null, regulatory_area: null, managed_area: null, landowner_permission: true };

describe('Profile persisted account data', () => {
  let http: HttpTestingController;
  let fixture: ComponentFixture<Profile>;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Profile], providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
    TestBed.inject(AuthService).ensureSession().subscribe();
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'testhunter', email: 'testhunter@example.com', first_name: 'Hunter', last_name: 'Example', is_staff: false });
    fixture = TestBed.createComponent(Profile);
    fixture.detectChanges();
    http.expectOne('/api/personal/preferences/').flush({ species: [1], managed_areas: [7], zones: [3] });
    http.expectOne('/api/personal/saved-searches/').flush([search]);
    http.expectOne('/api/catalog/').flush({
      land_types: [], zones: [{ id: 3, code: 'A', name: 'Zone A' }], dmus: [], regulatory_areas: [],
      managed_areas: [{ id: 7, name: 'Everglades', area_type: 'WMA' }]
    });
    http.expectOne('/api/species/').flush([{ id: 1, name: 'Wild Hog' }]);
    fixture.detectChanges();
    await fixture.whenStable();
  });
  afterEach(() => http.verify());

  it('shows the actual identity, saved selections and refreshable saved-search URL', () => {
    expect(fixture.nativeElement.textContent).toContain('Hunter Example');
    expect(fixture.nativeElement.textContent).toContain('testhunter@example.com');
    expect(fixture.nativeElement.textContent).not.toContain('Prototype');
    expect(fixture.componentInstance.preferences).toEqual({ species: [1], managed_areas: [7], zones: [3] });
    const link = fixture.nativeElement.querySelector('a[href^="/results"]');
    expect(link.getAttribute('href')).toContain('date=2026-11-03');
    expect(link.getAttribute('href')).toContain('landowner_permission=true');
  });

  it('persists edited preferences and reports server validation without erasing selections', () => {
    const component = fixture.componentInstance;
    component.preferences.species = [];
    component.savePreferences();
    http.expectOne('/api/auth/csrf/').flush({});
    const request = http.expectOne('/api/personal/preferences/');
    expect(request.request.body.species).toEqual([]);
    request.flush({ species: ['This selection is unavailable.'] }, { status: 400, statusText: 'Bad Request' });
    expect(component.error()).toContain('This selection is unavailable');
    expect(component.preferences.species).toEqual([]);
    expect(component.saving()).toBe(false);
  });

  it('renames and deletes saved searches only after successful server responses', () => {
    const component = fixture.componentInstance;
    component.editSearch(search);
    component.searchTitle = 'Updated weekend';
    component.renameSearch(search);
    http.expectOne('/api/auth/csrf/').flush({});
    const rename = http.expectOne('/api/personal/saved-searches/5/');
    expect(rename.request.method).toBe('PATCH');
    rename.flush({ ...search, title: 'Updated weekend' });
    expect(component.savedSearches()[0].title).toBe('Updated weekend');
    component.deleteSearch(search);
    http.expectOne('/api/auth/csrf/').flush({});
    const deletion = http.expectOne('/api/personal/saved-searches/5/');
    expect(component.savedSearches()).toHaveLength(1);
    deletion.flush(null, { status: 204, statusText: 'No Content' });
    expect(component.savedSearches()).toEqual([]);
  });

  it('clears private selections and saved searches immediately after logout', () => {
    TestBed.inject(AuthService).logout().subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/logout/').flush(null, { status: 204, statusText: 'No Content' });
    fixture.detectChanges();
    expect(fixture.componentInstance.savedSearches()).toEqual([]);
    expect(fixture.componentInstance.preferences).toEqual({ species: [], managed_areas: [], zones: [] });
    expect(fixture.nativeElement.textContent).not.toContain('Weekend hog');
    expect(fixture.nativeElement.textContent).not.toContain('testhunter@example.com');
  });
});
