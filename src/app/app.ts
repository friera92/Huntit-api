import { CommonModule } from '@angular/common';
import { Component, DestroyRef, HostListener, inject, OnInit, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from './services/auth.service';
import { apiErrorMessage } from './services/api-error';
import { catchError, finalize, of } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {
  readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  private sessionCheckPending = false;
  readonly logoutPending = signal(false);
  readonly logoutError = signal('');
  isMenuOpen = false;

  ngOnInit(): void {
    this.sessionCheckPending = true;
    this.auth.ensureSession().pipe(finalize(() => this.sessionCheckPending = false),
      takeUntilDestroyed(this.destroyRef)).subscribe();
  }

  @HostListener('window:focus')
  refreshVisibleSession(): void {
    if (document.visibilityState === 'hidden' || this.sessionCheckPending || this.logoutPending()) return;
    this.sessionCheckPending = true;
    this.auth.refreshSession().pipe(catchError(() => of(null)),
      finalize(() => this.sessionCheckPending = false), takeUntilDestroyed(this.destroyRef)).subscribe();
  }

  @HostListener('document:visibilitychange')
  visibilityChanged(): void {
    if (document.visibilityState === 'visible') this.refreshVisibleSession();
  }

  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen;
  }

  logout(): void {
    if (this.logoutPending()) return;
    this.logoutPending.set(true);
    this.logoutError.set('');
    this.auth.logout().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: () => {
        this.logoutPending.set(false);
        this.isMenuOpen = false;
        void this.router.navigate(['/']);
      },
      error: error => {
        this.logoutPending.set(false);
        this.logoutError.set(apiErrorMessage(error, 'Unable to log out. Please try again.'));
      }
    });
  }
}
