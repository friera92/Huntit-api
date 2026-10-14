import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRouteSnapshot, provideRouter, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { firstValueFrom, Observable } from 'rxjs';
import { authGuard } from './auth.guard';

describe('Profile authentication guard', () => {
  it('redirects guests to login with a return URL', async () => {
    TestBed.configureTestingModule({ providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] });
    const result = TestBed.runInInjectionContext(() => authGuard({} as ActivatedRouteSnapshot, { url: '/profile' } as RouterStateSnapshot)) as Observable<boolean | UrlTree>;
    const pending = firstValueFrom(result);
    const http = TestBed.inject(HttpTestingController);
    http.expectOne('/api/auth/me/').flush({ detail: 'Not authenticated.' }, { status: 401, statusText: 'Unauthorized' });
    expect(TestBed.inject(Router).serializeUrl(await pending as UrlTree)).toBe('/login?returnUrl=%2Fprofile');
    http.verify();
  });
});
