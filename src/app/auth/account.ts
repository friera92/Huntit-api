import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { apiErrorMessage } from '../services/api-error';

export function safeReturnUrl(router: Router, value: string | null): string {
  if (!value || !value.startsWith('/') || value.startsWith('//') || /[\\\u0000-\u001f]/.test(value)) return '/profile';
  try {
    const tree = router.parseUrl(value);
    const groups = Object.keys(tree.root.children);
    const primary = tree.root.children['primary'];
    const segments = primary?.segments.map(segment => segment.path) || [];
    if (groups.some(group => group !== 'primary') || Object.keys(primary?.children || {}).length || segments.length > 1) return '/profile';
    return ['', 'profile', 'log', 'licenses', 'results', 'settings'].includes(segments[0] || '') ? router.serializeUrl(tree) : '/profile';
  } catch { return '/profile'; }
}

@Component({
  selector: 'app-account',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './account.html',
  styleUrl: './account.css'
})
export class Account {
  private readonly auth = inject(AuthService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  readonly registerMode = this.route.snapshot.data['register'] === true;
  readonly pending = signal(false);
  readonly error = signal('');
  username = '';
  email = '';
  password = '';
  passwordConfirm = '';

  submit(form: NgForm): void {
    if (this.pending() || form.invalid) return;
    this.error.set('');
    if (!this.username.trim()) {
      this.error.set('Enter a username.');
      return;
    }
    if (this.registerMode && this.password !== this.passwordConfirm) {
      this.error.set('Passwords must match.');
      return;
    }
    this.pending.set(true);
    const request = this.registerMode
      ? this.auth.register({ username: this.username.trim(), email: this.email.trim(), password: this.password, password_confirm: this.passwordConfirm })
      : this.auth.login({ username: this.username.trim(), password: this.password });
    request.subscribe({
      next: () => {
        this.pending.set(false);
        form.resetForm();
        void this.router.navigateByUrl(safeReturnUrl(this.router, this.route.snapshot.queryParamMap.get('returnUrl')));
      },
      error: error => {
        this.pending.set(false);
        this.password = '';
        this.passwordConfirm = '';
        this.error.set(apiErrorMessage(error, 'Unable to complete your request. Please try again.'));
      }
    });
  }
}
