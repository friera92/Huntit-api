import { provideHttpClient, withXsrfConfiguration } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { AuthService, User } from './auth.service';

const user: User = { id: 1, username: 'testhunter', email: 'testhunter@example.com', first_name: 'Hunter', last_name: 'Example', is_staff: false };

describe('AuthService session integration', () => {
  let service: AuthService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withXsrfConfiguration({ cookieName: 'csrftoken', headerName: 'X-CSRFToken' })),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(AuthService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
    document.cookie = 'csrftoken=; Max-Age=0; path=/';
  });

  it('treats an unauthenticated session as a guest and shares the startup request', () => {
    const sessions: (User | null)[] = [];
    service.ensureSession().subscribe(value => sessions.push(value));
    service.ensureSession().subscribe(value => sessions.push(value));
    http.expectOne('/api/auth/me/').flush({ detail: 'Not authenticated.' }, { status: 401, statusText: 'Unauthorized' });
    expect(sessions).toEqual([null, null]);
    service.ensureSession().subscribe();
    http.expectNone('/api/auth/me/');
    expect(service.currentUser()).toBeNull();
  });

  it('fetches CSRF before login and uses the rotated cookie for logout', () => {
    service.login({ username: 'testhunter', password: 'example-password' }).subscribe();
    http.expectNone('/api/auth/login/');
    document.cookie = 'csrftoken=before-login; path=/';
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'before-login' });
    const login = http.expectOne('/api/auth/login/');
    expect(login.request.method).toBe('POST');
    expect(login.request.headers.get('X-CSRFToken')).toBe('before-login');
    login.flush(user);
    expect(service.currentUser()).toEqual(user);

    service.logout().subscribe();
    document.cookie = 'csrftoken=after-login; path=/';
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'after-login' });
    const logout = http.expectOne('/api/auth/logout/');
    expect(logout.request.headers.get('X-CSRFToken')).toBe('after-login');
    logout.flush(null, { status: 204, statusText: 'No Content' });
    expect(service.currentUser()).toBeNull();
  });

  it('registers through the CSRF endpoint and establishes the returned session', () => {
    const registration = { username: 'testhunter', email: user.email, password: 'example-password', password_confirm: 'example-password' };
    service.register(registration).subscribe();
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'token' });
    const request = http.expectOne('/api/auth/register/');
    expect(request.request.body).toEqual(registration);
    request.flush(user);
    expect(service.currentUser()).toEqual(user);
  });

  it('keeps a valid session when logout is rejected for CSRF', () => {
    service.ensureSession().subscribe();
    http.expectOne('/api/auth/me/').flush(user);
    const onError = vi.fn();
    service.logout().subscribe({ error: onError });
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'token' });
    http.expectOne('/api/auth/logout/').flush({ detail: 'CSRF failed.' }, { status: 403, statusText: 'Forbidden' });
    expect(service.currentUser()).toEqual(user);
    http.expectOne('/api/auth/me/').flush(user);
    expect(onError).toHaveBeenCalledWith(expect.objectContaining({ status: 403 }));
    expect(service.currentUser()).toEqual(user);
  });

  it.each([401, 403])('clears an expired session after logout %s only when the server confirms expiry', status => {
    service.ensureSession().subscribe();
    http.expectOne('/api/auth/me/').flush(user);
    const onComplete = vi.fn();
    service.logout().subscribe({ complete: onComplete });
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'token' });
    http.expectOne('/api/auth/logout/').flush({ detail: 'Authentication required.' }, { status, statusText: 'Unauthorized' });
    expect(service.currentUser()).toEqual(user);
    http.expectOne('/api/auth/me/').flush({ detail: 'Authentication required.' }, { status: 401, statusText: 'Unauthorized' });
    expect(service.currentUser()).toBeNull();
    expect(onComplete).toHaveBeenCalledOnce();
  });

  it('keeps the visible session if the verification request fails', () => {
    service.ensureSession().subscribe();
    http.expectOne('/api/auth/me/').flush(user);
    const onError = vi.fn();
    service.logout().subscribe({ error: onError });
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'token' });
    http.expectOne('/api/auth/logout/').flush({ detail: 'Forbidden.' }, { status: 403, statusText: 'Forbidden' });
    http.expectOne('/api/auth/me/').flush('Unavailable', { status: 503, statusText: 'Unavailable' });
    expect(service.currentUser()).toEqual(user);
    expect(onError).toHaveBeenCalledWith(expect.objectContaining({ status: 503 }));
  });

  it('does not overwrite a successful login with a late startup response', () => {
    service.ensureSession().subscribe();
    const startup = http.expectOne('/api/auth/me/');
    service.login({ username: 'testhunter', password: 'example-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'token' });
    http.expectOne('/api/auth/login/').flush(user);
    startup.flush({ detail: 'Not authenticated.' }, { status: 401, statusText: 'Unauthorized' });
    expect(service.currentUser()).toEqual(user);
  });

  it('cancels a password mutation if the initiating account changes during CSRF loading', () => {
    service.ensureSession().subscribe(); http.expectOne('/api/auth/me/').flush(user);
    service.changePassword({ current_password: 'old-password', new_password: 'new-password', new_password_confirm: 'new-password' }).subscribe();
    const pending = http.expectOne('/api/auth/csrf/');
    service.login({ username: 'second-user', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({}); http.expectOne('/api/auth/login/').flush({ ...user, id: 2, username: 'second-user' });
    pending.flush({}); http.expectNone('/api/auth/password/change/');
    expect(service.currentUser()?.id).toBe(2);
  });

  it('does not restore an old identity when a refresh finishes after logout', () => {
    service.ensureSession().subscribe(); http.expectOne('/api/auth/me/').flush(user);
    service.refreshSession().subscribe(); const pending = http.expectOne('/api/auth/me/');
    service.logout().subscribe(); http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/auth/logout/').flush(null, { status: 204, statusText: 'No Content' });
    pending.flush(user); expect(service.currentUser()).toBeNull();
  });
});
