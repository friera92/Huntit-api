import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NgForm } from '@angular/forms';
import { provideRouter, Router } from '@angular/router';
import { safeReturnUrl } from '../auth/account';
import { AccountSettings } from './account-settings';
import { AuthService } from '../services/auth.service';

describe('Account settings', () => {
  let fixture: ComponentFixture<AccountSettings>;
  let http: HttpTestingController;
  beforeEach(async () => {
    await TestBed.configureTestingModule({ imports: [AccountSettings],
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] }).compileComponents();
    fixture = TestBed.createComponent(AccountSettings); http = TestBed.inject(HttpTestingController); fixture.detectChanges();
  });
  afterEach(() => http.verify());

  it('requires matching passwords, sends the current password, and clears fields after success', () => {
    const component = fixture.componentInstance;
    component.currentPassword = 'old'; component.newPassword = 'new-strong-pass'; component.newPasswordConfirm = 'wrong';
    const resetForm = vi.fn(); const form = { invalid: false, resetForm } as unknown as NgForm;
    component.changePassword(form); expect(component.passwordError()).toContain('match'); http.expectNone('/api/auth/csrf/');
    component.newPasswordConfirm = component.newPassword; component.changePassword(form);
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'test' });
    const request = http.expectOne('/api/auth/password/change/'); expect(request.request.body.current_password).toBe('old');
    request.flush({ detail: 'Password changed.' }); expect(resetForm).toHaveBeenCalled(); expect(component.passwordPending()).toBe(false);
  });

  it('does not reset data without explicit selection and confirmation', () => {
    const component = fixture.componentInstance; component.clearPreferences = true; component.resetData();
    http.expectNone('/api/auth/csrf/'); component.confirmation = 'RESET MY DATA'; component.archiveHarvests = true; component.resetData();
    http.expectOne('/api/auth/csrf/').flush({ csrfToken: 'test' });
    const request = http.expectOne('/api/personal/reset/'); expect(request.request.body.harvests).toBe('archive');
    expect(request.request.body.preferences).toBe(true); expect(request.request.body.licenses).toBe(false);
    request.flush({}); expect(component.confirmation).toBe(''); expect(component.dataSuccess()).toContain('restored');
  });

  it('preserves local result filters after login and rejects external or auxiliary destinations', () => {
    const router = TestBed.inject(Router);
    expect(safeReturnUrl(router, '/results?species=2&date=2026-10-12')).toBe('/results?species=2&date=2026-10-12');
    for (const value of ['https://example.invalid', '//example.invalid', '/\\example.invalid', '/login', '/(popup:results)']) {
      expect(safeReturnUrl(router, value)).toBe('/profile');
    }
  });

  it('cancels a pending private export and clears form fields after an account switch', () => {
    const component = fixture.componentInstance;
    component.currentPassword = 'private-old-password'; component.confirmation = 'RESET MY DATA';
    component.exportData();
    const pending = http.expectOne('/api/personal/export/');
    TestBed.inject(AuthService).login({ username: 'second-user', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({}); http.expectOne('/api/auth/login/').flush({ id: 2, username: 'second-user' });
    fixture.detectChanges();
    expect(pending.cancelled).toBe(true); expect(component.dataPending()).toBe(false);
    expect(component.currentPassword).toBe(''); expect(component.confirmation).toBe(''); expect(component.dataSuccess()).toBe('');
  });

  it('does not issue a reset when the account changes while obtaining CSRF', () => {
    const component = fixture.componentInstance;
    component.clearPreferences = true; component.confirmation = 'RESET MY DATA'; component.resetData();
    const pending = http.expectOne('/api/auth/csrf/');
    TestBed.inject(AuthService).login({ username: 'second-user', password: 'test-password' }).subscribe();
    http.expectOne('/api/auth/csrf/').flush({}); http.expectOne('/api/auth/login/').flush({ id: 2, username: 'second-user' });
    pending.flush({});
    http.expectNone('/api/personal/reset/');
    expect(component.dataPending()).toBe(false); expect(component.dataSuccess()).toBe('');
  });
});
