import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { App } from './app';
import { AuthService } from './services/auth.service';

describe('App', () => {
  let http: HttpTestingController;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });
  afterEach(() => { http.verify(); vi.restoreAllMocks(); });

  it('renders the HuntIt shell and account links for a guest', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    http.expectOne('/api/auth/me/').flush({ detail: 'Not authenticated.' }, { status: 401, statusText: 'Unauthorized' });
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.app-name')?.textContent).toContain('HuntIt');
    expect(compiled.textContent).toContain('Create Account');
    expect(compiled.textContent).not.toContain('Log Out');
  });

  it('shows the profile and logout actions for an authenticated session', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'testhunter', email: '', first_name: 'Hunter', last_name: 'Example', is_staff: false });
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Profile');
    expect(fixture.nativeElement.textContent).toContain('Log Out');
    expect(fixture.nativeElement.textContent).not.toContain('Create Account');
  });

  it('refreshes a resumed tab once while a session check is pending and clears an expired identity', () => {
    vi.spyOn(document, 'visibilityState', 'get').mockReturnValue('visible');
    const fixture = TestBed.createComponent(App); fixture.detectChanges();
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'testhunter' });
    fixture.componentInstance.refreshVisibleSession(); fixture.componentInstance.refreshVisibleSession();
    http.expectOne('/api/auth/me/').flush({}, { status: 401, statusText: 'Unauthorized' });
    expect(TestBed.inject(AuthService).currentUser()).toBeNull();
  });

  it('keeps identity after a temporary refresh failure and skips focus checks during logout', () => {
    vi.spyOn(document, 'visibilityState', 'get').mockReturnValue('visible');
    const fixture = TestBed.createComponent(App); fixture.detectChanges();
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'testhunter' });
    fixture.componentInstance.refreshVisibleSession();
    http.expectOne('/api/auth/me/').flush({}, { status: 503, statusText: 'Unavailable' });
    expect(TestBed.inject(AuthService).currentUser()?.id).toBe(1);
    fixture.componentInstance.logoutPending.set(true); fixture.componentInstance.refreshVisibleSession();
    http.expectNone('/api/auth/me/');
  });
});
