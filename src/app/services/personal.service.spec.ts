import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { PersonalService, SavedSearch, savedSearchQuery } from './personal.service';
import { AuthService } from './auth.service';

describe('Personal data HTTP contract', () => {
  let service: PersonalService;
  let http: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(PersonalService);
    http = TestBed.inject(HttpTestingController);
  });
  afterEach(() => http.verify());

  it('fetches a CSRF cookie before saving preferences and preserves numeric selections', () => {
    const value = { species: [1, 2], managed_areas: [7], zones: [3] };
    service.savePreferences(value).subscribe(data => expect(data).toEqual(value));
    http.expectNone('/api/personal/preferences/');
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'test' });
    const request = http.expectOne('/api/personal/preferences/');
    expect(request.request.method).toBe('PUT');
    expect(request.request.body).toEqual(value);
    request.flush(value);
  });

  it('does not issue a mutation when obtaining CSRF fails', () => {
    let failed = false;
    service.deleteLicense(12).subscribe({ error: () => failed = true });
    http.expectOne('/api/auth/csrf/').flush({}, { status: 503, statusText: 'Unavailable' });
    http.expectNone('/api/personal/licenses/12/');
    expect(failed).toBe(true);
  });

  it('loads archived harvests only when explicitly requested', () => {
    service.harvests(true).subscribe();
    const request = http.expectOne(request => request.url === '/api/personal/harvests/');
    expect(request.request.params.get('archived')).toBe('true');
    request.flush([]);
  });

  it('archives and restores the specified server record instead of removing browser memory only', () => {
    service.archiveHarvest(7).subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    const archive = http.expectOne('/api/personal/harvests/7/archive/');
    expect(archive.request.method).toBe('POST');
    archive.flush({ id: 7, archived_at: '2026-10-12T00:00:00Z' });
    service.restoreHarvest(7).subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    const restore = http.expectOne('/api/personal/harvests/7/restore/');
    expect(restore.request.method).toBe('POST');
    restore.flush({ id: 7, archived_at: null });
  });

  it('stores only saved-search inputs and reopens them as a fresh URL query', () => {
    const value: SavedSearch = {
      id: 8, title: 'Weekend', species: 2, land_type: 1, hunting_date: '2026-11-03',
      zone: 4, dmu: 12, regulatory_area: null, managed_area: null, landowner_permission: true
    };
    const { id, ...input } = value;
    service.saveSearch(input).subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    const request = http.expectOne('/api/personal/saved-searches/');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(input);
    expect(request.request.body['result']).toBeUndefined();
    request.flush(value);
    expect(savedSearchQuery(value)).toEqual({
      species: '2', land_type: '1', date: '2026-11-03', zone: '4', dmu: '12', landowner_permission: 'true'
    });
  });

  it('suppresses a pending personal response after the signed-in account changes', () => {
    let received = false;
    service.licenses().subscribe(() => received = true);
    const pending = http.expectOne('/api/personal/licenses/');
    TestBed.inject(AuthService).login({ username: 'second-user', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/login/').flush({ id: 2, username: 'second-user' });
    pending.flush([{ id: 9, name: 'Previous account license' }]);
    expect(received).toBe(false);
  });

  it('cancels a write if the account changes while the CSRF request is pending', () => {
    service.deleteLicense(9).subscribe();
    const pending = http.expectOne('/api/auth/csrf/');
    TestBed.inject(AuthService).login({ username: 'second-user', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/login/').flush({ id: 2, username: 'second-user' });
    pending.flush({});
    http.expectNone('/api/personal/licenses/9/');
  });

  it('confirms session expiration after a denied personal request', () => {
    const auth = TestBed.inject(AuthService);
    auth.ensureSession().subscribe();
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'first-user' });
    let failed = false;
    service.preferences().subscribe({ error: () => failed = true });
    http.expectOne('/api/personal/preferences/').flush({ detail: 'Authentication required.' }, { status: 403, statusText: 'Forbidden' });
    http.expectOne('/api/auth/me/').flush({ detail: 'Not authenticated.' }, { status: 401, statusText: 'Unauthorized' });
    expect(auth.currentUser()).toBeNull();
    expect(failed).toBe(true);
  });

  it('preserves a valid account after a CSRF denial', () => {
    const auth = TestBed.inject(AuthService);
    auth.ensureSession().subscribe();
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'first-user' });
    service.deleteLicense(9).subscribe({ error: () => {} });
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/personal/licenses/9/').flush({ detail: 'CSRF failed.' }, { status: 403, statusText: 'Forbidden' });
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'first-user' });
    expect(auth.currentUser()?.id).toBe(1);
  });
});
