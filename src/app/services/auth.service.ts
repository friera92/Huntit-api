import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { catchError, EMPTY, filter, finalize, Observable, of, shareReplay, switchMap, tap, throwError } from 'rxjs';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
}

export interface Registration {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly user = signal<User | null>(null);
  private sessionLoaded = false;
  private sessionRevision = 0;
  private sessionRequest?: Observable<User | null>;
  readonly currentUser = this.user.asReadonly();

  ensureSession(): Observable<User | null> {
    if (this.sessionLoaded) return of(this.user());
    if (!this.sessionRequest) {
      const revision = this.sessionRevision;
      this.sessionRequest = this.http.get<User>('/api/auth/me/').pipe(
        catchError(() => of(null)),
        tap(user => {
          if (revision === this.sessionRevision) {
            this.user.set(user);
            this.sessionLoaded = true;
          }
        }),
        finalize(() => { this.sessionRequest = undefined; }),
        shareReplay({ bufferSize: 1, refCount: false })
      );
    }
    return this.sessionRequest;
  }

  login(credentials: { username: string; password: string }): Observable<User> {
    return this.csrf().pipe(
      switchMap(() => this.http.post<User>('/api/auth/login/', credentials)),
      tap(user => this.setUser(user))
    );
  }

  register(registration: Registration): Observable<User> {
    return this.csrf().pipe(
      switchMap(() => this.http.post<User>('/api/auth/register/', registration)),
      tap(user => this.setUser(user))
    );
  }

  logout(): Observable<void> {
    return this.csrf().pipe(
      switchMap(() => this.http.post<void>('/api/auth/logout/', {})),
      tap(() => this.setUser(null)),
      catchError(error => {
        if (!(error instanceof HttpErrorResponse) || ![401, 403].includes(error.status)) {
          return throwError(() => error);
        }
        return this.refreshSession().pipe(
          switchMap(user => user ? throwError(() => error) : of(undefined))
        );
      })
    );
  }

  changePassword(passwords: { current_password: string; new_password: string; new_password_confirm: string }): Observable<{ detail: string }> {
    const ownerId = this.user()?.id;
    return this.csrf().pipe(
      switchMap(() => ownerId === this.user()?.id
        ? this.http.post<{ detail: string }>('/api/auth/password/change/', passwords) : EMPTY),
      filter(() => ownerId === this.user()?.id),
      catchError(error => {
        if (ownerId !== this.user()?.id) return EMPTY;
        if (error instanceof HttpErrorResponse && [401, 403].includes(error.status)) {
          return this.refreshSession().pipe(catchError(() => of(null)), switchMap(() => throwError(() => error)));
        }
        return throwError(() => error);
      })
    );
  }

  refreshSession(): Observable<User | null> {
    const revision = this.sessionRevision;
    return this.http.get<User>('/api/auth/me/').pipe(
      catchError(error => error instanceof HttpErrorResponse && error.status === 401
        ? of(null)
        : throwError(() => error)),
      tap(user => {
        if (revision === this.sessionRevision) this.setUser(user);
      })
    );
  }

  private csrf(): Observable<{ csrfToken: string }> {
    return this.http.get<{ csrfToken: string }>('/api/auth/csrf/');
  }

  private setUser(user: User | null): void {
    this.sessionRevision++;
    this.user.set(user);
    this.sessionLoaded = true;
  }
}
